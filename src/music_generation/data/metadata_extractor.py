from dataclasses import dataclass
from pathlib import Path
from tqdm import tqdm
import pandas as pd

from music_generation.data.genre_metadata_extractor import (
    GenreMetadataExtractor,
)


@dataclass(slots=True)
class TrackMetadataRecord:
    track_id: str
    midi_path: str
    artist_terms: list[str]
    musicbrainz_tags: list[str]


class MetadataExtractor:

    def __init__(self) -> None:
        self.genre_extractor = (GenreMetadataExtractor())

    def load_validation_index(self,validation_csv: str | Path,) -> dict[str, list[str]]:
        df = pd.read_csv(validation_csv)
        df = df[df["is_valid"]]
        grouped = df.groupby("track_id")["file_path"].apply(list).to_dict()
        return {str(k): [str(p) for p in v] for k, v in grouped.items()}

    def scan(self,h5_root: str | Path,validation_csv: str | Path,) -> list[TrackMetadataRecord]:

        validation_index = (self.load_validation_index(validation_csv))
        records: list[TrackMetadataRecord] = []

        for track_id, midi_paths in tqdm(
            validation_index.items(),
            desc="Extracting metadata",
            unit="track",
        ):

            h5_path = (
                Path(h5_root)
                / track_id[2]
                / track_id[3]
                / track_id[4]
                / f"{track_id}.h5"
            )

            if not h5_path.exists():
                continue

            (artist_terms,musicbrainz_tags,) = (self.genre_extractor.load_tags_from_h5(h5_path))

            if not artist_terms and not musicbrainz_tags:
                continue

            for midi_path in midi_paths:

                records.append(
                    TrackMetadataRecord(
                        track_id=track_id,
                        midi_path=midi_path,
                        artist_terms=artist_terms,
                        musicbrainz_tags=musicbrainz_tags,
                    )
                )

        print(f"Tracks processed: {len(validation_index):,}")
        print(f"Records created: {len(records):,}")
        return records

    def save_to_csv(self,records: list[TrackMetadataRecord],output_path: str | Path,) -> None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True,exist_ok=True,)

        pd.DataFrame(
            [
                {
                    "track_id": r.track_id,
                    "midi_path": r.midi_path,
                    "artist_terms": "|".join(
                        r.artist_terms
                    ),
                    "musicbrainz_tags": "|".join(
                        r.musicbrainz_tags
                    ),
                }
                for r in records
            ]
        ).to_csv(output_path,index=False,)
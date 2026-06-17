from dataclasses import dataclass
from pathlib import Path
from tqdm import tqdm
import pandas as pd

from music_generation.utils.utils import load_validation_index, load_tags_from_h5
from configs.dataset.metadata_extractor_config import TrackMetadataRecord




class MetadataExtractor:

    def scan(self,h5_root: str | Path,validation_csv: str | Path,) -> list[TrackMetadataRecord]:

        validation_index = load_validation_index(validation_csv)
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

            (artist_terms,musicbrainz_tags,) = (load_tags_from_h5(h5_path))

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
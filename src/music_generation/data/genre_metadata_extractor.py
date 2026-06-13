from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from tqdm import tqdm
import pandas as pd
import h5py

GENRE_TAGS = {
    "rock": {
        "rock",
        "classic rock",
        "alternative rock",
        "hard rock",
        "folk rock",
        "indie rock",
        "progressive rock",
        "punk",
        "punk rock",
        "new wave",
        "soft rock",
        "pop rock",
    },
    "pop": {
        "pop",
        "europop",
        "synthpop",
        "dance pop",
        "teen pop",
        "power pop",
        "indie pop",
    },
    "electronic": {
        "electronic",
        "electro",
        "house",
        "techno",
        "trance",
        "electronica",
        "downtempo",
        "ambient",
    },
    "jazz": {
        "jazz",
        "acid jazz",
        "smooth jazz",
        "latin jazz",
        "bebop",
        "fusion",
        "jazz fusion",
        "soul jazz",
    },
    "hip_hop": {
        "hip hop",
        "rap",
        "rnb",
        "hip-hop",
    },
}

@dataclass(slots=True)
class TrackGenreMetadata:
    track_id: str
    genres: list[str]
    genre_source: str | None
    scores: dict[str, int]
    artist_terms: list[str]
    musicbrainz_tags: list[str]


@dataclass(slots=True)
class MidiGenreRecord:
    track_id: str
    midi_path: str
    genres: list[str]
    genre_source: str | None


class GenreMetadataExtractor:
    """
    Extract normalized genres from LMD-Matched metadata.

    Supported genres:

        - rock
        - pop
        - electronic
        - jazz
        - hip_hop

    Genre source priority:

        1. MusicBrainz tags
        2. Artist terms
    """


    def score_tags(self,tags: Iterable[str],) -> dict[str, int]:
        scores = {genre: 0 for genre in GENRE_TAGS}
        for tag in map(str.lower, tags):
            for genre, keywords in GENRE_TAGS.items():
                scores[genre] += sum(
                    keyword in tag
                    for keyword in keywords
                )
        return scores


    def assign_genre(self,tags: Iterable[str],) -> tuple[list[str], dict[str, int]]:
        scores = self.score_tags(tags)
        max_score = max(scores.values())
        if max_score == 0:
            return [], scores
        genres = [genre for genre, score in scores.items() if score == max_score]
        return genres, scores


    def _decode_tags(self,values,) -> list[str]:
        return [
            (v.decode("utf-8", errors="ignore")if isinstance(v, bytes)else str(v)).strip().lower() for v in values
        ]


    def load_tags_from_h5(self,h5_path: str | Path,) -> tuple[list[str], list[str]]:

        with h5py.File(h5_path, "r") as h5_file:
            def read(dataset_path: str) -> list[str]:
                try:
                    return self._decode_tags(h5_file[dataset_path][:])  # type: ignore
                except Exception:
                    return []
            artist_terms = read("metadata/artist_terms")
            musicbrainz_tags = read("musicbrainz/artist_mbtags")
        return artist_terms, musicbrainz_tags


    def extract_track_genre(self,track_id: str,h5_path: str | Path,) -> TrackGenreMetadata:

        artist_terms, musicbrainz_tags = self.load_tags_from_h5(h5_path)
        tags = musicbrainz_tags if musicbrainz_tags else artist_terms
        genre_source = "musicbrainz_tags" if musicbrainz_tags else "artist_terms"
        genres, scores = self.assign_genre(tags)
        genre_source = genre_source if genres else None

        return TrackGenreMetadata(
            track_id=track_id,
            genres=genres,
            genre_source=genre_source,
            scores=scores,
            artist_terms=artist_terms,
            musicbrainz_tags=musicbrainz_tags,
        )


    def find_track_ids(self,h5_root: str | Path,) -> list[tuple[str, Path]]:

        h5_root = Path(h5_root)
        return [(h5_file.stem, h5_file) for h5_file in h5_root.rglob("*.h5")]


    def load_validation_index(self,validation_csv: str | Path,) -> dict[str, list[str]]:
        df = pd.read_csv(validation_csv)
        df = df[df["is_valid"]]
        return df.groupby("track_id")["file_path"].apply(list).to_dict()  # type: ignore


    def create_records_for_track(
        self,
        track_id: str,
        h5_path: str | Path,
        validation_index: dict[str, list[str]],
    ) -> list[MidiGenreRecord]:

        metadata = self.extract_track_genre(track_id, h5_path)
        if not metadata.genres:
            return []
        midi_paths = validation_index.get(
            track_id,
            [],
        )
        return [
            MidiGenreRecord(
                track_id=track_id,
                midi_path=midi_path,
                genres=metadata.genres,
                genre_source=metadata.genre_source,
            )
            for midi_path in midi_paths
        ]


    def scan_dataset(
        self,
        h5_root: str | Path,
        validation_csv: str | Path,
        limit: int | None = None,
    ) -> list[MidiGenreRecord]:

        records: list[MidiGenreRecord] = []
        validation_index = self.load_validation_index(validation_csv)
        valid_track_ids = set(validation_index.keys())
        track_ids = [
            (track_id, h5_path)
            for track_id, h5_path in self.find_track_ids(h5_root)
            if track_id in valid_track_ids
        ]
        print(f"Valid tracks: {len(track_ids):,}")
        if limit is not None:
            track_ids = track_ids[:limit]
        for track_id, h5_path in tqdm(track_ids, desc="Scanning tracks", unit="track"):
            records.extend(
                self.create_records_for_track(
                    track_id=track_id,
                    h5_path=h5_path,
                    validation_index=validation_index,
                )
            )
        return records


    def save_records_to_csv(
        self,
        records: list[MidiGenreRecord],
        output_path: str | Path,
    ) -> None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        pd.DataFrame(
            [
                {
                    "track_id": r.track_id,
                    "midi_path": r.midi_path,
                    "genres": "|".join(r.genres),
                    "genre_source": r.genre_source,
                }
                for r in records
            ]
        ).to_csv(output_path, index=False)


if __name__ == "__main__":
    extractor = GenreMetadataExtractor()

    records = extractor.scan_dataset(
        h5_root="data/raw/lmd_matched_h5",
        validation_csv="data/interim/midi_validation_results.csv",
        limit=100,
    )

    print(f"Found {len(records)} MIDI files with genre metadata")
    print(records[:5])

    for record in records:
        print(record)

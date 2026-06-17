from __future__ import annotations

from pathlib import Path
from typing import Iterable
from tqdm import tqdm
import pandas as pd

from configs.dataset.genre_metadata_extractor_config import (
    GenreMetadataConstants,
    GenreMetadataDefaults,
    TrackGenreMetadata,
    MidiGenreRecord,
)


class GenreMetadataExtractor:
    """
    Extract normalized genres from track metadata CSV.

    Reads artist_terms and musicbrainz_tags produced by MetadataExtractor
    and assigns normalized genres via keyword scoring.

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

    def score_tags(self, tags: Iterable[str]) -> dict[str, int]:
        scores = {genre: 0 for genre in GenreMetadataConstants.GENRE_TAGS}
        for tag in map(str.lower, tags):
            for genre, keywords in GenreMetadataConstants.GENRE_TAGS.items():
                scores[genre] += sum(keyword in tag for keyword in keywords)
        return scores

    def assign_genre(self, tags: Iterable[str]) -> tuple[list[str], dict[str, int]]:
        scores = self.score_tags(tags)
        max_score = max(scores.values())
        if max_score == 0:
            return [], scores
        genres = [genre for genre, score in scores.items() if score == max_score]
        return genres, scores

    def extract_track_genre(
        self,
        track_id: str,
        artist_terms: list[str],
        musicbrainz_tags: list[str],
    ) -> TrackGenreMetadata:
        tags = musicbrainz_tags if musicbrainz_tags else artist_terms
        genre_source = (
            GenreMetadataDefaults.MUSICBRAINZ_SOURCE
            if musicbrainz_tags
            else GenreMetadataDefaults.ARTIST_TERMS_SOURCE
        )
        genres, scores = self.assign_genre(tags)

        return TrackGenreMetadata(
            track_id=track_id,
            genres=genres,
            genre_source=genre_source if genres else None,
            scores=scores,
            artist_terms=artist_terms,
            musicbrainz_tags=musicbrainz_tags,
        )

    @staticmethod
    def _parse_pipe_column(value: object) -> list[str]:
        if pd.isna(value):  # type: ignore[arg-type]
            return []
        return [t.strip() for t in str(value).split("|") if t.strip()]

    def scan_dataset(
        self,
        track_metadata_csv: str | Path,
        limit: int | None = None,
    ) -> list[MidiGenreRecord]:
        """
        Assign genres to every row in track_metadata.csv.

        Parameters
        ----------
        track_metadata_csv:
            Output of MetadataExtractor — contains track_id, midi_path,
            artist_terms, musicbrainz_tags.
        limit:
            If set, process only the first N rows (useful for testing).
        """
        df = pd.read_csv(track_metadata_csv)

        if limit is not None:
            df = df.head(limit)

        records: list[MidiGenreRecord] = []

        for row in tqdm(
            df.itertuples(index=False),
            total=len(df),
            desc="Extracting genres",
            unit="row",
        ):
            artist_terms = self._parse_pipe_column(row.artist_terms)
            musicbrainz_tags = self._parse_pipe_column(row.musicbrainz_tags)

            metadata = self.extract_track_genre(
                track_id=str(row.track_id),
                artist_terms=artist_terms,
                musicbrainz_tags=musicbrainz_tags,
            )

            if not metadata.genres:
                continue

            records.append(
                MidiGenreRecord(
                    track_id=str(row.track_id),
                    midi_path=str(row.midi_path),
                    genres=metadata.genres,
                    genre_source=metadata.genre_source,
                )
            )

        print(f"Rows processed:      {len(df):,}")
        print(f"Records with genre:  {len(records):,}")
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

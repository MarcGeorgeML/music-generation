# uv run python scripts/run_genre_metadata_extraction.py

from pathlib import Path
from collections import Counter

from music_generation.data.genre_metadata_extractor import GenreMetadataExtractor


def main() -> None:
    extractor = GenreMetadataExtractor()

    records = extractor.scan_dataset(
        h5_root="data/raw/lmd_matched_h5",
        validation_csv="data/interim/midi_validation_results.csv",
    )

    genre_counter = Counter()

    for record in records:
        for genre in record.genres:
            genre_counter[genre] += 1

    print("\nGenre Counts")
    for genre, count in genre_counter.items():
        print(f"{genre}: {count:,}")

    extractor.save_records_to_csv(records, Path("data/interim/genre_metadata.csv"))
    print(f"Saved {len(records)} records")


if __name__ == "__main__":
    main()

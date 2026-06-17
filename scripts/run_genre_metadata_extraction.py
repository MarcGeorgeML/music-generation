# uv run python scripts/run_genre_metadata_extraction.py

from collections import Counter

from music_generation.data.genre_metadata_extractor import GenreMetadataExtractor
from configs.dataset.genre_metadata_extractor_config import GenreMetadataPaths
from configs.dataset.metadata_extractor_config import MetadataExtractorPaths


def main() -> None:
    extractor = GenreMetadataExtractor()

    records = extractor.scan_dataset(track_metadata_csv=MetadataExtractorPaths.OUTPUT_CSV,)

    genre_counter = Counter()
    for record in records:
        for genre in record.genres:
            genre_counter[genre] += 1

    print("\nGenre Counts")
    for genre, count in genre_counter.most_common():
        print(f"{genre}: {count:,}")

    extractor.save_records_to_csv(records, GenreMetadataPaths.OUTPUT_CSV)
    print(f"\nSaved {len(records):,} records to {GenreMetadataPaths.OUTPUT_CSV}")


if __name__ == "__main__":
    main()
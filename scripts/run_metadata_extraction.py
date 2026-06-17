# uv run python scripts/run_metadata_extraction.py

from music_generation.data.metadata_extractor import MetadataExtractor
from configs.dataset.genre_metadata_extractor_config import GenreMetadataPaths
from configs.dataset.metadata_extractor_config import MetadataExtractorPaths

if __name__ == "__main__":
    extractor = MetadataExtractor()
    records = extractor.scan(h5_root=GenreMetadataPaths.H5_ROOT, validation_csv=MetadataExtractorPaths.VALIDATION_CSV)
    extractor.save_to_csv(records, MetadataExtractorPaths.OUTPUT_CSV)
    print(f"Saved {len(records):,} records")
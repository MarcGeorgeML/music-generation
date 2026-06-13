from music_generation.data.metadata_extractor import (
    MetadataExtractor,
)

extractor = MetadataExtractor()

records = extractor.scan(
    h5_root="data/raw/lmd_matched_h5",
    validation_csv="data/interim/midi_validation_results.csv",
)

extractor.save_to_csv(
    records,
    "data/interim/track_metadata.csv",
)

print(f"Saved {len(records):,} records")
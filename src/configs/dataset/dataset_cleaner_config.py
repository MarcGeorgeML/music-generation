from dataclasses import dataclass
from pathlib import Path

from configs.dataset.common_config import DatasetFiles, DatasetPaths, ProcessedDatasetFiles


@dataclass(frozen=True)
class DatasetCleanerPaths:
    VALIDATION_CSV: Path = DatasetPaths.INTERIM_DIR / DatasetFiles.MIDI_VALIDATION_CSV
    GENRE_CSV: Path = DatasetPaths.INTERIM_DIR / DatasetFiles.GENRE_METADATA_CSV
    INSTRUMENT_CSV: Path = DatasetPaths.INTERIM_DIR / DatasetFiles.INSTRUMENT_FAMILIES_CSV
    TRACK_METADATA_CSV: Path = DatasetPaths.INTERIM_DIR / DatasetFiles.TRACK_METADATA_CSV

    CLEAN_DATASET_CSV: Path = DatasetPaths.PROCESSED_DIR / ProcessedDatasetFiles.CLEAN_DATASET_CSV
    CLEAN_GENRE_CSV: Path = DatasetPaths.PROCESSED_DIR / ProcessedDatasetFiles.CLEAN_GENRE_METADATA_CSV
    CLEAN_INSTRUMENT_CSV: Path = DatasetPaths.PROCESSED_DIR / ProcessedDatasetFiles.CLEAN_INSTRUMENT_FAMILIES_CSV
    REPORT_JSON: Path = DatasetPaths.REPORTS_DIR / ProcessedDatasetFiles.DATASET_CLEANING_REPORT_JSON


@dataclass(frozen=True)
class DatasetCleanerConstants:
    SUPPORTED_INSTRUMENT_FAMILIES: frozenset[str] = frozenset(
        {
            "drums",
            "bass",
            "guitar",
            "piano",
            "strings",
        }
    )

@dataclass(slots=True)
class DatasetCleaningConfig:
    validation_csv: Path = DatasetCleanerPaths.VALIDATION_CSV
    genre_csv: Path = DatasetCleanerPaths.GENRE_CSV
    instrument_csv: Path = DatasetCleanerPaths.INSTRUMENT_CSV
    track_metadata_csv: Path = DatasetCleanerPaths.TRACK_METADATA_CSV

    clean_dataset_csv: Path = DatasetCleanerPaths.CLEAN_DATASET_CSV
    clean_genre_csv: Path = DatasetCleanerPaths.CLEAN_GENRE_CSV
    clean_instrument_csv: Path = DatasetCleanerPaths.CLEAN_INSTRUMENT_CSV

    report_json: Path = DatasetCleanerPaths.REPORT_JSON

    # Filled in later after duration analysis
    min_duration_seconds: float | None = None
    max_duration_seconds: float | None = None


@dataclass(slots=True)
class DatasetCleaningReport:
    initial_files: int
    retained_files: int
    retention_rate: float

    removed_invalid_files: int
    removed_missing_genres: int
    removed_empty_instrument_assignments: int

    removed_short_files: int = 0
    removed_long_files: int = 0
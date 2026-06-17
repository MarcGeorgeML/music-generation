from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DatasetPaths:
    RAW_DIR: Path = Path("data/raw")
    INTERIM_DIR: Path = Path("data/interim")
    PROCESSED_DIR: Path = Path("data/processed")
    REPORTS_DIR: Path = Path("data/reports")


@dataclass(frozen=True)
class DatasetFiles:
    TRACK_METADATA_CSV: str = "track_metadata.csv"
    GENRE_METADATA_CSV: str = "genre_metadata.csv"
    INSTRUMENT_FAMILIES_CSV: str = "instrument_families.csv"
    MIDI_VALIDATION_CSV: str = "midi_validation_results.csv"
    MIDI_DURATIONS_CSV: str = "midi_durations.csv"
    MIDI_STATISTICS_JSON: str = "midi_statistics.json"


@dataclass(frozen=True)
class ProcessedDatasetFiles:
    CLEAN_DATASET_CSV: str = "clean_dataset.csv"
    CLEAN_GENRE_METADATA_CSV: str = "clean_genre_metadata.csv"
    CLEAN_INSTRUMENT_FAMILIES_CSV: str = "clean_instrument_families.csv"
    DATASET_CLEANING_REPORT_JSON: str = "dataset_cleaning_report.json"


@dataclass(frozen=True)
class RawDatasetFiles:
    LMD_MATCHED_H5_DIR: Path = (DatasetPaths.RAW_DIR / "lmd_matched_h5")
    LMD_MATCHED_DIR: Path = (DatasetPaths.RAW_DIR / "lmd_matched")
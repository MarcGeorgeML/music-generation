from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DatasetStatisticsConstants:
    SUPPORTED_INSTRUMENT_ORDER: tuple[str, ...] = (
        "drums",
        "bass",
        "guitar",
        "piano",
        "strings",
        "other",
    )


@dataclass(frozen=True)
class DatasetStatisticsOutputs:
    SUMMARY_JSON: str = "dataset_summary.json"
    GENRE_STATISTICS_CSV: str = "genre_statistics.csv"
    INSTRUMENT_STATISTICS_CSV: str = "instrument_statistics.csv"
    GENRE_INSTRUMENT_STATISTICS_CSV: str = (
        "genre_instrument_statistics.csv"
    )


@dataclass(frozen=True)
class DatasetStatisticsConfig:
    track_metadata_path: Path
    genre_metadata_path: Path
    instrument_families_path: Path
    validation_results_path: Path
    output_dir: Path


@dataclass(frozen=True)
class DatasetStatisticsResult:
    summary_path: Path
    genre_statistics_path: Path
    instrument_statistics_path: Path
    genre_instrument_statistics_path: Path

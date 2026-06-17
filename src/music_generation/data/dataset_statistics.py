"""Dataset statistics generation for the music generation project.

This module is metadata-only: it reads the approved interim CSV artifacts and
produces dataset-level summary reports without parsing MIDI files.
"""

from __future__ import annotations


import json
from pathlib import Path
from tqdm import tqdm
import pandas as pd

from configs.dataset.common_config import DatasetFiles, DatasetPaths

from configs.dataset.dataset_statistics_config import (
    DatasetStatisticsConstants, 
    DatasetStatisticsOutputs, 
    DatasetStatisticsConfig, 
    DatasetStatisticsResult
)
from music_generation.utils.utils import parse_list_value


def _ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing required input file: {path}")
    return pd.read_csv(path)





def _parse_instrument_family_list(value: object) -> list[str]:
    families = [family.lower() for family in parse_list_value(value)]
    return [family for family in families if family]


def _split_genres_frame(df: pd.DataFrame, genre_col: str = "genres") -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Genres"):
        genres = parse_list_value(row.get(genre_col))
        for genre in genres:
            rows.append(
                {
                    "track_id": row.get("track_id"),
                    "midi_path": row.get("midi_path"),
                    "genre": str(genre).strip(),
                }
            )
    return pd.DataFrame(rows)


def _split_instrument_frame(df: pd.DataFrame, family_col: str = "instrument_families") -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Instrument families"):
        families = _parse_instrument_family_list(row.get(family_col))
        for family in families:
            rows.append(
                {
                    "track_id": row.get("track_id"),
                    "midi_path": row.get("midi_path"),
                    "instrument_family": family,
                }
            )
    return pd.DataFrame(rows)


def _ensure_midi_path_column(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    if "midi_path" not in frame.columns:
        for alias in ("file_path", "path", "filepath"):
            if alias in frame.columns:
                frame = frame.rename(columns={alias: "midi_path"})
                break
    if "midi_path" not in frame.columns:
        raise ValueError(
            "All input tables must include a 'midi_path' or compatible path column."
        )
    return frame


def _normalize_joined_frame(
    track_metadata: pd.DataFrame,
    genre_metadata: pd.DataFrame,
    instrument_families: pd.DataFrame,
    validation_results: pd.DataFrame,
) -> pd.DataFrame:
    base = track_metadata.copy()

    genre_metadata = _ensure_midi_path_column(genre_metadata)
    instrument_families = _ensure_midi_path_column(instrument_families)
    validation_results = _ensure_midi_path_column(validation_results)

    genre_cols = [
        c
        for c in ("track_id", "midi_path", "genres", "genre_source")
        if c in genre_metadata.columns
    ]
    instrument_cols = [
        c
        for c in ("track_id", "midi_path", "instrument_families")
        if c in instrument_families.columns
    ]
    validation_cols = [
        c
        for c in ("file_id", "track_id", "midi_path", "is_valid", "failure_reason")
        if c in validation_results.columns
    ]

    merged = base.merge(
        genre_metadata[genre_cols].drop_duplicates(
            subset=[c for c in ["midi_path"] if c in genre_cols]
        ),
        on=[
            c
            for c in ["track_id", "midi_path"]
            if c in base.columns and c in genre_metadata.columns
        ],
        how="left",
        suffixes=("", "_genre"),
    )
    merged = merged.merge(
        instrument_families[instrument_cols].drop_duplicates(
            subset=[c for c in ["midi_path"] if c in instrument_cols]
        ),
        on=[
            c
            for c in ["track_id", "midi_path"]
            if c in merged.columns and c in instrument_families.columns
        ],
        how="left",
        suffixes=("", "_inst"),
    )
    merged = merged.merge(
        validation_results[validation_cols].drop_duplicates(
            subset=[c for c in ["midi_path"] if c in validation_cols]
        ),
        on=[
            c
            for c in ["track_id", "midi_path"]
            if c in merged.columns and c in validation_results.columns
        ],
        how="left",
        suffixes=("", "_val"),
    )
    return merged


def _compute_genre_statistics(
    genre_rows: pd.DataFrame,
    total_files: int,
) -> pd.DataFrame:
    if genre_rows.empty:
        return pd.DataFrame(
            columns=[
                "genre",
                "example_count",
                "unique_midi_files",
                "percentage_of_examples",
                "percentage_of_files",
            ]
        )

    total_examples = len(genre_rows)
    grouped = (
        genre_rows.groupby("genre", dropna=False)
        .agg(
            example_count=("midi_path", "size"),
            unique_midi_files=("midi_path", "nunique"),
        )
        .reset_index()
    )
    grouped["percentage_of_examples"] = (
        grouped["example_count"] / total_examples * 100.0
    )
    grouped["percentage_of_files"] = (
        grouped["unique_midi_files"] / max(total_files, 1) * 100.0
    )
    grouped = grouped.sort_values(
        ["example_count", "genre"], ascending=[False, True]
    ).reset_index(drop=True)
    return grouped


def _compute_instrument_statistics(
    inst_rows: pd.DataFrame,
    total_files: int,
) -> pd.DataFrame:
    if inst_rows.empty:
        return pd.DataFrame(
            columns=[
                "instrument_family",
                "example_count",
                "unique_midi_files",
                "percentage_of_examples",
                "percentage_of_files",
            ]
        )

    total_examples = len(inst_rows)
    grouped = (
        inst_rows.groupby("instrument_family", dropna=False)
        .agg(
            example_count=("midi_path", "size"),
            unique_midi_files=("midi_path", "nunique"),
        )
        .reset_index()
    )
    grouped["percentage_of_examples"] = (
        grouped["example_count"] / total_examples * 100.0
    )
    grouped["percentage_of_files"] = (
        grouped["unique_midi_files"] / max(total_files, 1) * 100.0
    )
    grouped["instrument_family"] = pd.Categorical(
        grouped["instrument_family"],
        categories=DatasetStatisticsConstants.SUPPORTED_INSTRUMENT_ORDER,
        ordered=True,
    )
    grouped = grouped.sort_values(
        ["example_count", "instrument_family"], ascending=[False, True]
    ).reset_index(drop=True)
    grouped["instrument_family"] = grouped["instrument_family"].astype(str)
    return grouped


def _compute_genre_instrument_statistics(
    genre_rows: pd.DataFrame,
    inst_rows: pd.DataFrame,
) -> pd.DataFrame:
    if genre_rows.empty or inst_rows.empty:
        return pd.DataFrame(
            columns=[
                "genre",
                "instrument_family",
                "example_count",
                "unique_midi_files",
                "percentage_of_joint_examples",
            ]
        )

    merged = genre_rows.merge(inst_rows, on=["track_id", "midi_path"], how="inner")
    total_joint = len(merged)
    grouped = (
        merged.groupby(["genre", "instrument_family"], dropna=False)
        .agg(
            example_count=("midi_path", "size"),
            unique_midi_files=("midi_path", "nunique"),
        )
        .reset_index()
    )
    grouped["percentage_of_joint_examples"] = (
        grouped["example_count"] / max(total_joint, 1) * 100.0
    )
    grouped = grouped.sort_values(
        ["example_count", "genre", "instrument_family"], ascending=[False, True, True]
    ).reset_index(drop=True)
    return grouped


def _compute_instrument_family_combinations(joined: pd.DataFrame) -> pd.DataFrame:
    if "midi_path" not in joined.columns:
        return pd.DataFrame(
            columns=["instrument_combination", "midi_file_count", "percentage_of_files"]
        )

    rows = []
    for _, row in tqdm(
        joined[["midi_path", "instrument_families"]]
        .drop_duplicates(subset=["midi_path"])
        .iterrows(),
        total=joined["midi_path"].nunique(dropna=True),
        desc="Instrument combinations",
    ):
        families = _parse_instrument_family_list(row.get("instrument_families"))
        if not families:
            continue
        ordered = [
            family
            for family in DatasetStatisticsConstants.SUPPORTED_INSTRUMENT_ORDER
            if family in set(families)
        ]
        combination = " + ".join(ordered)
        rows.append(
            {"instrument_combination": combination, "midi_path": row["midi_path"]}
        )

    if not rows:
        return pd.DataFrame(
            columns=["instrument_combination", "midi_file_count", "percentage_of_files"]
        )

    combo_df = pd.DataFrame(rows)
    grouped = (
        combo_df.groupby("instrument_combination", dropna=False)
        .agg(midi_file_count=("midi_path", "nunique"))
        .reset_index()
    )
    total_files = combo_df["midi_path"].nunique(dropna=True)
    grouped["percentage_of_files"] = (
        grouped["midi_file_count"] / max(total_files, 1) * 100.0
    )
    grouped = grouped.sort_values(
        ["midi_file_count", "instrument_combination"], ascending=[False, True]
    ).reset_index(drop=True)
    return grouped


def _build_summary(
    joined: pd.DataFrame,
    genre_stats: pd.DataFrame,
    instrument_stats: pd.DataFrame,
    genre_instrument_stats: pd.DataFrame,
    combination_stats: pd.DataFrame,
) -> dict:
    validation_counts = {}
    if "is_valid" in joined.columns:
        counts = (
            joined["is_valid"].dropna().astype(str).value_counts(dropna=False).to_dict()
        )
        validation_counts = {str(k): int(v) for k, v in counts.items()}

    avg_families_per_midi = 0.0
    if "instrument_families" in joined.columns and not joined.empty:
        family_counts = joined["instrument_families"].apply(
            lambda x: len(_parse_instrument_family_list(x))
        )
        avg_families_per_midi = (
            float(family_counts.mean()) if not family_counts.empty else 0.0
        )

    summary = {
        "total_midi_files": int(joined["midi_path"].nunique(dropna=True)),
        "total_unique_tracks": (
            int(joined["track_id"].nunique(dropna=True))
            if "track_id" in joined.columns
            else None
        ),
        "validation_counts": validation_counts,
        "genre_count": (
            int(genre_stats["genre"].nunique()) if not genre_stats.empty else 0
        ),
        "instrument_family_count": (
            int(instrument_stats["instrument_family"].nunique())
            if not instrument_stats.empty
            else 0
        ),
        "genre_instrument_pair_count": int(len(genre_instrument_stats)),
        "average_instrument_families_per_midi": avg_families_per_midi,
        "most_common_instrument_combinations": combination_stats.head(10).to_dict(
            orient="records"
        ),
    }
    return summary


def generate_dataset_statistics(
    config: DatasetStatisticsConfig,
) -> DatasetStatisticsResult:
    """Generate dataset statistics reports from approved interim metadata."""

    _ensure_output_dir(config.output_dir)

    track_metadata = _read_csv(config.track_metadata_path)
    genre_metadata = _read_csv(config.genre_metadata_path)
    instrument_families = _read_csv(config.instrument_families_path)
    validation_results = _read_csv(config.validation_results_path)
    print(f"Track metadata rows: {len(track_metadata):,}")
    print(f"Genre metadata rows: {len(genre_metadata):,}")
    print(f"Instrument family rows: {len(instrument_families):,}")
    print(f"Validation rows: {len(validation_results):,}")

    joined = _normalize_joined_frame(
        track_metadata, genre_metadata, instrument_families, validation_results
    )
    print("[1/4] Expanding genre metadata...")
    genre_rows = _split_genres_frame(joined)

    print("[2/4] Expanding instrument metadata...")
    inst_rows = _split_instrument_frame(joined)

    total_files = joined["midi_path"].nunique(dropna=True)

    genre_stats = _compute_genre_statistics(
        genre_rows,
        total_files,
    )

    instrument_stats = _compute_instrument_statistics(
        inst_rows,
        total_files,
    )

    genre_instrument_stats = _compute_genre_instrument_statistics(
        genre_rows,
        inst_rows,
    )
    combination_stats = _compute_instrument_family_combinations(joined)
    summary = _build_summary(
        joined, genre_stats, instrument_stats, genre_instrument_stats, combination_stats
    )

    summary_path = config.output_dir / DatasetStatisticsOutputs.SUMMARY_JSON
    genre_path = config.output_dir / DatasetStatisticsOutputs.GENRE_STATISTICS_CSV
    instrument_path = config.output_dir / DatasetStatisticsOutputs.INSTRUMENT_STATISTICS_CSV
    genre_instrument_path = config.output_dir / DatasetStatisticsOutputs.GENRE_INSTRUMENT_STATISTICS_CSV

    summary_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    genre_stats.to_csv(genre_path, index=False)
    instrument_stats.to_csv(instrument_path, index=False)
    genre_instrument_stats.to_csv(genre_instrument_path, index=False)

    return DatasetStatisticsResult(
        summary_path=summary_path,
        genre_statistics_path=genre_path,
        instrument_statistics_path=instrument_path,
        genre_instrument_statistics_path=genre_instrument_path,
    )


def default_config(project_root: Path | None = None) -> DatasetStatisticsConfig:
    root = project_root or Path.cwd()
    interim_dir = root / DatasetPaths.INTERIM_DIR
    reports_dir = root / DatasetPaths.REPORTS_DIR
    return DatasetStatisticsConfig(
        track_metadata_path=interim_dir / DatasetFiles.TRACK_METADATA_CSV,
        genre_metadata_path=interim_dir / DatasetFiles.GENRE_METADATA_CSV,
        instrument_families_path=interim_dir / DatasetFiles.INSTRUMENT_FAMILIES_CSV,
        validation_results_path=interim_dir / DatasetFiles.MIDI_VALIDATION_CSV,
        output_dir=reports_dir,
    )
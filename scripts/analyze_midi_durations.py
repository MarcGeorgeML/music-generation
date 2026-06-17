# uv run python scripts/analyze_midi_durations.py

from pathlib import Path
import json
from tqdm import tqdm
import numpy as np
import pandas as pd
import pretty_midi

from configs.dataset.common_config import DatasetPaths, DatasetFiles


VALIDATION_CSV = Path(DatasetPaths.INTERIM_DIR / DatasetFiles.MIDI_VALIDATION_CSV)
OUTPUT_CSV = Path(DatasetPaths.INTERIM_DIR / DatasetFiles.MIDI_DURATIONS_CSV)
OUTPUT_JSON = Path(DatasetPaths.REPORTS_DIR / DatasetFiles.MIDI_STATISTICS_JSON)


def get_duration_seconds(midi_path: str) -> float:
    try:
        midi = pretty_midi.PrettyMIDI(midi_path)
        return float(midi.get_end_time())
    except Exception:
        return np.nan


def main():
    validation_df = pd.read_csv(VALIDATION_CSV)
    valid_df = validation_df[ validation_df["is_valid"] == True].copy()
    durations = []
    failed_files = 0
    total = len(valid_df)

    for row in tqdm(
        valid_df.itertuples(index=False),
        total=len(valid_df),
        desc="Analyzing MIDI durations",
    ):
        try:
            duration = get_duration_seconds(str(row.file_path)) 
            durations.append({"midi_path": row.file_path,"duration_seconds": duration,})
        except Exception as e:
            failed_files += 1
    duration_df = pd.DataFrame(durations)
    duration_df = duration_df.dropna()
    duration_df.to_csv(OUTPUT_CSV, index=False)
    series = duration_df["duration_seconds"]
    values = series.to_numpy(dtype=np.float64)

    stats = {
        "count": int(series.count()),
        "min_seconds": float(series.min()),
        "max_seconds": float(series.max()),
        "mean_seconds": float(series.mean()),
        "median_seconds": float(series.median()),
        "std_seconds": float(series.std()),
        "p01": float(np.percentile(values, 1)),
        "p05": float(np.percentile(values, 5)),
        "p10": float(np.percentile(values, 10)),
        "p25": float(np.percentile(values, 25)),
        "p50": float(np.percentile(values, 50)),
        "p75": float(np.percentile(values, 75)),
        "p90": float(np.percentile(values, 90)),
        "p95": float(np.percentile(values, 95)),
        "p99": float(np.percentile(values, 99)),
    }

    q1 = np.percentile(values, 25)
    q3 = np.percentile(values, 75)
    iqr = q3 - q1
    stats["iqr_lower_bound"] = float(q1 - 1.5 * iqr)
    stats["iqr_upper_bound"] = float(q3 + 1.5 * iqr)
    stats["recommended_short_threshold"] = stats["p01"]
    stats["recommended_long_threshold"] = stats["p99"]
    print("\nDuration Statistics")
    print("=" * 60)

    for key, value in stats.items():
        print(f"{key}: {value}")

    with open(OUTPUT_JSON, "w") as f:
        json.dump(stats, f, indent=2)

    print(f"\nSaved durations -> {OUTPUT_CSV}")
    print(f"Saved statistics -> {OUTPUT_JSON}")
    print(f"Failed files: {failed_files} out of {total}")


if __name__ == "__main__":
    main()

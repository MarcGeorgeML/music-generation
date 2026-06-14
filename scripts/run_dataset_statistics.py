# uv run python scripts/run_dataset_statistics.py

from __future__ import annotations

from pathlib import Path

from music_generation.data.dataset_statistics import default_config, generate_dataset_statistics


if __name__ == "__main__":
    result = generate_dataset_statistics(default_config(Path.cwd()))
    print("Generated dataset statistics reports:")
    print(f"- {result.summary_path}")
    print(f"- {result.genre_statistics_path}")
    print(f"- {result.instrument_statistics_path}")
    print(f"- {result.genre_instrument_statistics_path}")

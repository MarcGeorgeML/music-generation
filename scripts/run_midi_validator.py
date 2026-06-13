from pathlib import Path
import pandas as pd
from tqdm import tqdm

from music_generation.data.dataset_loader import DatasetLoader
from music_generation.data.midi_validator import MidiValidator


def main() -> None:
    """
    Run MIDI validation across the entire dataset and save results.
    """

    loader = DatasetLoader()
    validator = MidiValidator()

    print("Scanning dataset...")
    dataset_df = loader.scan("data/raw/lmd_matched")
    # print(len(dataset_df))
    print(f"Found {len(dataset_df):,} MIDI files")
    results = []
    rows = zip(
        dataset_df["file_id"],
        dataset_df["track_id"],
        dataset_df["path"],
    )

    for file_id, track_id, path in tqdm(
        rows,
        total=len(dataset_df),
        desc="Validating MIDI files",
    ):
        result = validator.validate_file(str(path))
        results.append(
            {
                "file_id": file_id,
                "track_id": track_id,
                "file_path": result.file_path,
                "is_valid": result.is_valid,
                "failure_reason": result.failure_reason,
            }
        )

    results_df = pd.DataFrame(results)
    output_dir = Path("data/interim")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "midi_validation_results.csv"
    results_df.to_csv(
        output_path,
        index=False,
    )
    valid_count = results_df["is_valid"].sum()
    invalid_count = len(results_df) - valid_count
    print("\nValidation Complete")
    print(f"Valid files:   {valid_count:,}")
    print(f"Invalid files: {invalid_count:,}")
    print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    main()

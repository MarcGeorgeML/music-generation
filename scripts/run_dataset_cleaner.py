# uv run python scripts/run_dataset_cleaner.py

from music_generation.data.dataset_cleaner import DatasetCleaner, DatasetCleaningConfig


def main() -> None:
    config = DatasetCleaningConfig()
    cleaner = DatasetCleaner(config)
    cleaner.run()


if __name__ == "__main__":
    main()

# uv run python scripts/scan_dataset.py

from music_generation.data.dataset_loader import DatasetLoader
from configs.dataset.common_config import RawDatasetFiles

loader = DatasetLoader()
df = loader.scan(str(RawDatasetFiles.LMD_MATCHED_DIR))
print(df.head())
print()
print(f"Total MIDI files: {len(df)}")

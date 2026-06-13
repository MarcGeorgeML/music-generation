from music_generation.data.dataset_loader import DatasetLoader

loader = DatasetLoader()

df = loader.scan("data/raw/lmd_matched")

print(df.head())
print()
print(f"Total MIDI files: {len(df)}")

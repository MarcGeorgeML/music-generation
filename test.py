import pandas as pd

df = pd.read_csv(
    "data/interim/midi_validation_results.csv"
)

# print(df.head())
# print()

# print("Rows:", len(df))
# print()

# print("Columns:")
# print(df.columns.tolist())
# print()

# print("Valid files:")
# print(df["is_valid"].value_counts())
# print()

# print("Failure reasons:")
# print(df["failure_reason"].value_counts(dropna=False))
# print()

# print("Unique track IDs:")
# print(df["track_id"].nunique())

valid_df = df[df["is_valid"]]

print(
    "Tracks with valid MIDI:",
    valid_df["track_id"].nunique()
)

print(
    "Total tracks:",
    df["track_id"].nunique()
)
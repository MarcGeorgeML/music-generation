import pandas as pd

df = pd.read_csv(
    "data/interim/genre_metadata.csv"
)

print(df.head())
print()

print("Rows:", len(df))

print(
    df["genres"]
    .str.split("|", regex=False)
    .explode()
    .value_counts()
)
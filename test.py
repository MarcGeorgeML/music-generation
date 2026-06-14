import pandas as pd

df = pd.read_csv("data/interim/instrument_families.csv")

print(df.columns)
print(df["instrument_families"].head(20).tolist())
import pandas as pd

df = pd.read_csv(
    "data/interim/instrument_families.csv"
)

families = [
    "drums",
    "bass",
    "guitar",
    "piano",
    "strings",
    "other",
]

for family in families:
    count = (
        df["instrument_families"]
        .str.contains(family)
        .sum()
    )

    print(
        f"{family}: "
        f"{count:,}"
    )
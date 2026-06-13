from collections import Counter
import pandas as pd


GENRE_GROUPS = {
    "rock": {
        "rock",
        "classic rock",
        "alternative rock",
        "hard rock",
        "folk rock",
        "indie rock",
        "progressive rock",
        "punk",
        "punk rock",
        "new wave",
        "soft rock",
        "pop rock",
    },
    "pop": {
        "pop",
        "europop",
        "synthpop",
        "dance pop",
        "teen pop",
    },
    "electronic": {
        "electronic",
        "electro",
        "house",
        "techno",
        "trance",
        "electronica",
        "downtempo",
        "ambient",
    },
    "jazz": {
        "jazz",
        "bebop",
        "fusion",
        "soul jazz",
        "latin jazz",
        "acid jazz",
        "smooth jazz",
    },
    "hip_hop": {
        "hip hop",
        "rap",
        "rnb",
    },
    "country": {
        "country",
    },
    "folk": {
        "folk",
    },
    "blues": {
        "blues",
    },
    "classical": {
        "classical",
    },
    "metal": {
        "metal",
        "heavy metal",
    },
}


def extract_tags(row: str) -> list[str]:
    if pd.isna(row):
        return []

    return [
        tag.strip().lower()
        for tag in row.split("|")
        if tag.strip()
    ]


df = pd.read_csv("data/interim/track_metadata.csv")
genre_counter = Counter()

for tags_string in df["artist_terms"]:
    tags = extract_tags(tags_string)
    matched_genres = set()
    for genre, genre_tags in GENRE_GROUPS.items():
        if any(tag in genre_tags for tag in tags):
            matched_genres.add(genre)

    for genre in matched_genres:
        genre_counter[genre] += 1


print("\nNORMALIZED GENRE COUNTS\n")
for genre, count in genre_counter.most_common():
    print(f"{count:>8}  {genre}")
# uv run python scripts/analyze_tags.py

from collections import Counter
import pandas as pd

from configs.dataset.common_config import DatasetPaths, DatasetFiles


df = pd.read_csv(str(DatasetPaths.INTERIM_DIR / DatasetFiles.GENRE_METADATA_CSV))
artist_counter = Counter()
mb_counter = Counter()


for tags in df["artist_terms"].fillna(""):
    for tag in tags.split("|"):
        tag = tag.strip().lower()
        if tag:
            artist_counter[tag] += 1


for tags in df["musicbrainz_tags"].fillna(""):
    for tag in tags.split("|"):
        tag = tag.strip().lower()
        if tag:
            mb_counter[tag] += 1


print("\nTOP 100 ARTIST TERMS\n")
for tag, count in artist_counter.most_common(50):
    print(f"{count:>8}  {tag}")


print("\nTOP 100 MUSICBRAINZ TAGS\n")
for tag, count in mb_counter.most_common(50):
    print(f"{count:>8}  {tag}")
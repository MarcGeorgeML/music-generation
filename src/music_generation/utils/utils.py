import pandas as pd
from pathlib import Path
import json
import ast
import h5py

def load_validation_index(validation_csv: str | Path,) -> dict[str, list[str]]:
    df = pd.read_csv(validation_csv)
    df = df[df["is_valid"]]
    grouped = df.groupby("track_id")["file_path"].apply(list).to_dict()
    return {str(k): [str(p) for p in v] for k, v in grouped.items()}


def _decode_tags(values) -> list[str]:
    return [
        (v.decode("utf-8", errors="ignore")if isinstance(v, bytes)else str(v)).strip().lower() for v in values
    ]


def load_tags_from_h5(h5_path: str | Path,) -> tuple[list[str], list[str]]:

    with h5py.File(h5_path, "r") as h5_file:
        def read(dataset_path: str) -> list[str]:
            try:
                return _decode_tags(h5_file[dataset_path][:])  # type: ignore
            except Exception:
                return []
        artist_terms = read("metadata/artist_terms")
        musicbrainz_tags = read("musicbrainz/artist_mbtags")
    return artist_terms, musicbrainz_tags


def parse_list_value(value: object) -> list[str]:
    """Parse list-like metadata stored as CSV strings.

    Accepted formats:
    - Python list literal: "['Pop', 'Rock']"
    - JSON list: '["Pop", "Rock"]'
    - Delimited strings: "Pop; Rock" or "Pop, Rock"
    - Single token strings: "Pop"
    - Empty / null values -> []
    """

    if value is None or (isinstance(value, float) and pd.isna(value)):
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]

    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "null", "[]"}:
        return []

    parsed: object = text
    if (text.startswith("[") and text.endswith("]")) or (
        text.startswith("(") and text.endswith(")")
    ):
        for loader in (json.loads, ast.literal_eval):
            try:
                parsed = loader(text)
                break
            except Exception:
                continue

    if isinstance(parsed, (list, tuple, set)):
        return [str(item).strip() for item in parsed if str(item).strip()]

    for delimiter in ("|", ";", ","):
        if delimiter in text:
            return [part.strip() for part in text.split(delimiter) if part.strip()]

    return [text]
from dataclasses import dataclass
from configs.dataset.common_config import DatasetFiles, DatasetPaths, RawDatasetFiles


class GenreMetadataConstants:
    GENRE_TAGS: dict[str, set[str]] = {
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
            "power pop",
            "indie pop",
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
            "acid jazz",
            "smooth jazz",
            "latin jazz",
            "bebop",
            "fusion",
            "jazz fusion",
            "soul jazz",
        },
        "hip_hop": {
            "hip hop",
            "rap",
            "rnb",
            "hip-hop",
        },
    }


@dataclass(frozen=True)
class GenreMetadataDefaults:
    TEST_LIMIT: int = 100

    MUSICBRAINZ_SOURCE: str = "musicbrainz_tags"
    ARTIST_TERMS_SOURCE: str = "artist_terms"


@dataclass(frozen=True)
class GenreMetadataPaths:
    H5_ROOT = RawDatasetFiles.LMD_MATCHED_H5_DIR
    VALIDATION_CSV = DatasetPaths.INTERIM_DIR / DatasetFiles.MIDI_VALIDATION_CSV
    OUTPUT_CSV = DatasetPaths.INTERIM_DIR / DatasetFiles.GENRE_METADATA_CSV


@dataclass(slots=True)
class TrackGenreMetadata:
    track_id: str
    genres: list[str]
    genre_source: str | None
    scores: dict[str, int]
    artist_terms: list[str]
    musicbrainz_tags: list[str]


@dataclass(slots=True)
class MidiGenreRecord:
    track_id: str
    midi_path: str
    genres: list[str]
    genre_source: str | None

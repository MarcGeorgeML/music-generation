from dataclasses import dataclass

from configs.dataset.common_config import (
    DatasetFiles,
    DatasetPaths,
)


@dataclass(frozen=True)
class MetadataExtractorPaths:
    VALIDATION_CSV = DatasetPaths.INTERIM_DIR / DatasetFiles.MIDI_VALIDATION_CSV
    OUTPUT_CSV = DatasetPaths.INTERIM_DIR / DatasetFiles.TRACK_METADATA_CSV


@dataclass(slots=True)
class TrackMetadataRecord:
    track_id: str
    midi_path: str
    artist_terms: list[str]
    musicbrainz_tags: list[str]


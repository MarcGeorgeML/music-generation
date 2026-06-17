from __future__ import annotations

import pandas as pd

from music_generation.data.dataset_cleaner import DatasetCleaner, DatasetCleaningConfig
from configs.dataset.common_config import ProcessedDatasetFiles


def test_removes_invalid_files(tmp_path):
    validation_csv = tmp_path / "validation.csv"
    genre_csv = tmp_path / "genres.csv"
    instrument_csv = tmp_path / "instruments.csv"
    track_csv = tmp_path / "tracks.csv"

    pd.DataFrame(
        {
            "file_path": [
                "valid.mid",
                "invalid.mid",
            ],
            "is_valid": [
                True,
                False,
            ],
        }
    ).to_csv(validation_csv, index=False)

    pd.DataFrame(
        {
            "midi_path": [
                "valid.mid",
                "invalid.mid",
            ],
            "genres": [
                "rock",
                "rock",
            ],
        }
    ).to_csv(genre_csv, index=False)

    pd.DataFrame(
        {
            "midi_path": [
                "valid.mid",
                "invalid.mid",
            ],
            "instrument_families": [
                "drums|bass",
                "drums|bass",
            ],
        }
    ).to_csv(instrument_csv, index=False)

    pd.DataFrame(
        {
            "midi_path": [
                "valid.mid",
                "invalid.mid",
            ],
        }
    ).to_csv(track_csv, index=False)

    config = DatasetCleaningConfig(
        validation_csv=validation_csv,
        genre_csv=genre_csv,
        instrument_csv=instrument_csv,
        track_metadata_csv=track_csv,
        clean_dataset_csv=tmp_path / "clean_dataset.csv",
        clean_genre_csv=tmp_path / "clean_genres.csv",
        clean_instrument_csv=tmp_path / "clean_instruments.csv",
        report_json=tmp_path / "report.json",
    )

    report = DatasetCleaner(config).run()

    clean_df = pd.read_csv(config.clean_dataset_csv)

    assert len(clean_df) == 1
    assert clean_df.iloc[0]["midi_path"] == "valid.mid"

    assert report.removed_invalid_files == 1

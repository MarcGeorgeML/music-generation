from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'src'))

from music_generation.data.dataset_statistics import default_config, generate_dataset_statistics


def test_generate_dataset_statistics(tmp_path: Path) -> None:
    data_dir = tmp_path / 'data' / 'interim'
    data_dir.mkdir(parents=True)

    pd.DataFrame(
        {
            'track_id': [1, 1, 2],
            'midi_path': ['a.mid', 'b.mid', 'c.mid'],
        }
    ).to_csv(data_dir / 'track_metadata.csv', index=False)

    pd.DataFrame(
        {
            'track_id': [1, 1, 2],
            'midi_path': ['a.mid', 'b.mid', 'c.mid'],
            'genres': ["['Pop', 'Rock']", "['Pop']", "['Jazz']"],
            'genre_source': ['x', 'x', 'x'],
        }
    ).to_csv(data_dir / 'genre_metadata.csv', index=False)

    pd.DataFrame(
        {
            'track_id': [1, 1, 2],
            'midi_path': ['a.mid', 'b.mid', 'c.mid'],
            'instrument_families': ["['piano', 'bass']", "['drums']", "['piano', 'strings']"],
        }
    ).to_csv(data_dir / 'instrument_families.csv', index=False)

    pd.DataFrame(
        {
            'file_id': [10, 11, 12],
            'track_id': [1, 1, 2],
            'midi_path': ['a.mid', 'b.mid', 'c.mid'],
            'is_valid': [True, True, False],
            'failure_reason': ['', '', 'parse_error'],
        }
    ).to_csv(data_dir / 'midi_validation_results.csv', index=False)

    result = generate_dataset_statistics(
        default_config(tmp_path)
    )

    assert result.summary_path.exists()
    assert result.genre_statistics_path.exists()
    assert result.instrument_statistics_path.exists()
    assert result.genre_instrument_statistics_path.exists()

from music_generation.utils.utils import load_validation_index


def test_load_validation_index(tmp_path):
    import pandas as pd

    validation_csv = tmp_path / "validation.csv"

    pd.DataFrame(
        {
            "track_id": ["TRAAA", "TRAAA", "TRBBB"],
            "file_path": [
                "a.mid",
                "b.mid",
                "c.mid",
            ],
            "is_valid": [
                True,
                True,
                False,
            ],
        }
    ).to_csv(validation_csv, index=False)

    result = load_validation_index(validation_csv)

    assert result == {
        "TRAAA": [
            "a.mid",
            "b.mid",
        ]
    }
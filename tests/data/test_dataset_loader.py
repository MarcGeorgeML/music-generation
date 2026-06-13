from music_generation.data.dataset_loader import DatasetLoader


def test_scan(tmp_path):
    track_dir = (tmp_path / "TRAAAGR128F425B14B")
    track_dir.mkdir()
    midi_file = (track_dir / "example.mid")
    midi_file.touch()
    loader = DatasetLoader()
    df = loader.scan(tmp_path)
    assert len(df) == 1
    assert df.iloc[0]["track_id"] == "TRAAAGR128F425B14B"
import pretty_midi
from music_generation.data.midi_validator import MidiValidator

validator = MidiValidator()


def test_parse_error(tmp_path):
    file_path = tmp_path / "broken.mid"
    file_path.write_text("not a midi")
    result = validator.validate_file(file_path)
    assert result.failure_reason == "parse_error"


def test_no_instruments(tmp_path):
    midi = pretty_midi.PrettyMIDI()
    file_path = tmp_path / "empty.mid"
    midi.write(str(file_path))
    result = validator.validate_file(file_path)
    assert result.failure_reason == "no_instruments"


def test_valid_midi(tmp_path):
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)
    instrument.notes.append(
        pretty_midi.Note(
            velocity=100,
            pitch=60,
            start=0.0,
            end=1.0,
        )
    )
    midi.instruments.append(instrument)
    file_path = tmp_path / "valid.mid"
    midi.write(str(file_path))
    result = validator.validate_file(file_path)
    assert result.is_valid
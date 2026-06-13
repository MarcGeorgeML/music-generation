from dataclasses import dataclass
from pathlib import Path

import pretty_midi


@dataclass(slots=True)
class MidiValidationResult:
    file_path: str
    is_valid: bool
    failure_reason: str | None


class MidiValidator:
    """
    Validates MIDI files for minimum dataset requirements.

    Validation Rules:
        1. MIDI must load successfully.
        2. MIDI must contain at least one instrument.
        3. MIDI must contain at least one note.
    """

    PARSE_ERROR = "parse_error"
    NO_INSTRUMENTS = "no_instruments"
    NO_NOTES = "no_notes"

    def validate_file(self,midi_path: str | Path,) -> MidiValidationResult:
        """
        Validate a single MIDI file.

        Parameters
        ----------
        midi_path : str | Path
            Path to the MIDI file.

        Returns
        -------
        MidiValidationResult
            Validation outcome.
        """
        midi_path = Path(midi_path)

        try:
            midi = pretty_midi.PrettyMIDI(str(midi_path))
        except Exception:
            return MidiValidationResult(
                file_path=str(midi_path),
                is_valid=False,
                failure_reason=self.PARSE_ERROR,
            )

        instrument_count = len(midi.instruments)
        note_count = sum(len(instrument.notes) for instrument in midi.instruments)

        if instrument_count == 0:
            return MidiValidationResult(
                file_path=str(midi_path),
                is_valid=False,
                failure_reason=self.NO_INSTRUMENTS,
            )

        if note_count == 0:
            return MidiValidationResult(
                file_path=str(midi_path),
                is_valid=False,
                failure_reason=self.NO_NOTES,
            )

        return MidiValidationResult(
            file_path=str(midi_path),
            is_valid=True,
            failure_reason=None,
        )

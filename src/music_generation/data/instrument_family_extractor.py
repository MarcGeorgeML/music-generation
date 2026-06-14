from dataclasses import dataclass
import pretty_midi


FAMILY_ORDER = [
    "drums",
    "bass",
    "guitar",
    "piano",
    "strings",
    "other",
]


@dataclass(slots=True)
class InstrumentFamilyResult:
    track_id: str
    midi_path: str
    instrument_families: list[str]


class InstrumentFamilyExtractor:
    PIANO_PROGRAMS = range(0, 8)
    GUITAR_PROGRAMS = range(24, 32)
    BASS_PROGRAMS = range(32, 40)
    STRINGS_PROGRAMS = range(40, 52)

    @classmethod
    def program_to_family(cls, program: int) -> str:
        if program in cls.PIANO_PROGRAMS:
            return "piano"

        if program in cls.GUITAR_PROGRAMS:
            return "guitar"

        if program in cls.BASS_PROGRAMS:
            return "bass"

        if program in cls.STRINGS_PROGRAMS:
            return "strings"

        return "other"

    @classmethod
    def instrument_to_family(cls,instrument: pretty_midi.Instrument,) -> str:
        if instrument.is_drum:
            return "drums"
        return cls.program_to_family(instrument.program)

    @classmethod
    def sort_families(cls,families: set[str],) -> list[str]:
        return [
            family
            for family in FAMILY_ORDER
            if family in families
        ]

    def extract_families(self,midi_path: str,) -> list[str]:
        midi = pretty_midi.PrettyMIDI(midi_path)
        families: set[str] = set()
        for instrument in midi.instruments:
            families.add(self.instrument_to_family(instrument))
        return self.sort_families(families)
    
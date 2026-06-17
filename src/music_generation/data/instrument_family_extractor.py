from dataclasses import dataclass
import pretty_midi


from configs.dataset.instrument_family_extractor_config import InstrumentFamilyConstants





class InstrumentFamilyExtractor:

    @classmethod
    def program_to_family(cls, program: int) -> str:
        if program in InstrumentFamilyConstants.PIANO_PROGRAMS:
            return "piano"

        if program in InstrumentFamilyConstants.GUITAR_PROGRAMS:
            return "guitar"

        if program in InstrumentFamilyConstants.BASS_PROGRAMS:
            return "bass"

        if program in InstrumentFamilyConstants.STRINGS_PROGRAMS:
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
            for family in InstrumentFamilyConstants.FAMILY_ORDER
            if family in families
        ]

    def extract_families(self,midi_path: str,) -> list[str]:
        try:
            midi = pretty_midi.PrettyMIDI(midi_path)
        except Exception:
            return []
        families: set[str] = set()
        for instrument in midi.instruments:
            families.add(self.instrument_to_family(instrument))
        return self.sort_families(families)
    
import pretty_midi

from music_generation.data.instrument_family_extractor import InstrumentFamilyExtractor


def test_program_to_piano():
    assert InstrumentFamilyExtractor.program_to_family(0) == "piano"


def test_program_to_guitar():
    assert InstrumentFamilyExtractor.program_to_family(24) == "guitar"


def test_program_to_bass():
    assert InstrumentFamilyExtractor.program_to_family(32) == "bass"


def test_program_to_strings():
    assert InstrumentFamilyExtractor.program_to_family(40) == "strings"


def test_program_to_other():
    assert InstrumentFamilyExtractor.program_to_family(80) == "other"


def test_drum_detection():
    instrument = pretty_midi.Instrument(
        program=0,
        is_drum=True,
    )

    assert InstrumentFamilyExtractor.instrument_to_family(instrument) == "drums"


def test_non_drum_detection():
    instrument = pretty_midi.Instrument(program=24,is_drum=False,)
    assert InstrumentFamilyExtractor.instrument_to_family(instrument) == "guitar"


def test_family_ordering():
    families = {"piano","drums","bass",}
    ordered = InstrumentFamilyExtractor.sort_families(families)
    assert ordered == ["drums","bass","piano",]


def test_family_ordering_with_all_families():
    families = {
        "other",
        "strings",
        "piano",
        "guitar",
        "bass",
        "drums",
    }

    ordered = InstrumentFamilyExtractor.sort_families(families)

    assert ordered == [
        "drums",
        "bass",
        "guitar",
        "piano",
        "strings",
        "other",
    ]

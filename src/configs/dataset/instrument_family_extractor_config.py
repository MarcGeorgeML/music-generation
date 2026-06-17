from dataclasses import dataclass


@dataclass(frozen=True)
class InstrumentFamilyConstants:
    FAMILY_ORDER: tuple[str, ...] = (
        "drums",
        "bass",
        "guitar",
        "piano",
        "strings",
        "other",
    )

    PIANO_PROGRAMS: range = range(0, 8)
    GUITAR_PROGRAMS: range = range(24, 32)
    BASS_PROGRAMS: range = range(32, 40)
    STRINGS_PROGRAMS: range = range(40, 52)
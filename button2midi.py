
from evdev import ecodes

T8_NOTES = {
    'BASS DRUM': 36,
    'SNARE DRUM': 38,
    'HAND CLAP': 50,
    'TOM': 47,
    'CLOSED HIHAT': 42,
    'OPEN HIHAT': 46
}

def get_t8_map() -> dict:
    return T8_NOTES

def get_midi_map() -> dict:
    return {
        ecodes.BTN_Y: T8_NOTES['SNARE DRUM'],
        ecodes.BTN_B: T8_NOTES['CLOSED HIHAT'],
        ecodes.BTN_Z: T8_NOTES['OPEN HIHAT'],
        ecodes.BTN_A: T8_NOTES['HAND CLAP'],
        ecodes.BTN_TL2: T8_NOTES['TOM']
    }

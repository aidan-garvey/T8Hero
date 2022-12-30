
from evdev import InputDevice, categorize, ecodes
import mido

import button2midi

STRUM_UP = ecodes.BTN_MODE
STRUM_DOWN = ecodes.BTN_THUMBL

mido.set_backend('mido.backends.rtmidi')

midiport: mido.ports.BaseOutput = None
for dev in mido.get_output_names():
    if dev.find('T-8') >= 0:
        midiport = mido.open_output(dev)

if midiport is None:
    print("Error: midi output device not found")
    exit()

guitar = InputDevice('/dev/input/event9')
print(guitar)

midinotes = button2midi.get_midi_map()
t8notes = button2midi.get_t8_map()

for event in guitar.read_loop():
    # if event.type == ecodes.EV_BTN:
    if event.code == STRUM_DOWN:
        midiport.send(mido.Message('note_on', note=t8notes['BASS DRUM']))
    elif event.code == STRUM_UP:
        for keycode in guitar.active_keys():
            note = midinotes.get(keycode)
            if note is not None:
                midiport.send(mido.Mesage('note_on', note=note))

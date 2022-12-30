
from evdev import InputDevice, categorize, ecodes
import mido

import button2midi

STRUM_UP = ecodes.BTN_MODE
STRUM_DOWN = ecodes.BTN_THUMBL
CHANNEL = 9 # t-8 uses channel 10 (1-indexed), mido is 0-indexed

mido.set_backend('mido.backends.rtmidi')

midiport: mido.ports.BaseOutput = None
for dev in mido.get_output_names():
    if dev.find('T-8') >= 0:
        midiport = mido.open_output(dev)

if midiport is None:
    print("Error: midi output device not found")
    exit()

print(midiport)

guitar = InputDevice('/dev/input/event9')
print(guitar)

midinotes = button2midi.get_midi_map()
t8notes = button2midi.get_t8_map()
# map button codes to mido messages
midimsgs = {x: mido.Message('note_on', channel=CHANNEL, note=midinotes[x]) for x in midinotes.keys()}
bass_msg = mido.Message('note_on', channel=CHANNEL, note=t8notes['BASS DRUM'])

for event in guitar.read_loop():
    if event.value != 0 and (event.code == STRUM_DOWN or event.code == STRUM_UP):
        sent = 0
        for keycode in guitar.active_keys():
            msg = midimsgs.get(keycode)
            if msg is not None:
                sent += 1
                midiport.send(msg)
        # if no instruments are being held, use bass by default
        if sent == 0:
            midiport.send(bass_msg)

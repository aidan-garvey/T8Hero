'''
config.py

Run this script to set up your controller for use with T8Hero

Settings configured by this script:
* which device to use as the controller
* controller buttons
* MIDI note bindings
* output device
* output channel
'''

import time
import json

from evdev import InputDevice, categorize, ecodes
import evdev
import mido

mido.set_backend('mido.backends.rtmidi')

print('''
 _____    ___    _   _
|_   _|  ( _ )  | | | | ___ _ __ ___
  | |___ / _ \  | |_| |/ _ | '__/ _ \ 
  | |___| (_) | |  _  |  __| | | (_) |
  |_|    \___/  |_| |_|\___|_|  \___/
''')

print('---- Configuration ----\nPress CTRL+C at any time to quit')

print('\nAvailable controllers:')
index = 0
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for i in range(len(devices)):
    print(f'{i}: {devices[i].name}')

devindex = int(input('Enter the number of the device you want to use'))
if devindex < 0 or devindex >= len(devices):
    print('Error: device number was incorrect')
    exit()

selected_dev = devices[devindex]
devpath = selected_dev.path

is_rockband = input('Is the controller a Rockband guitar (i.e. does it have two sets of fret buttons)? [y/n]').lower().startswith('y')

buttons = ['Strum up', 'Strum down', 'Green', 'Red', 'Yellow', 'Blue', 'Orange']
bindings = {}

print('Button configuration -- hit the following buttons', end='')
if is_rockband:
    print(' (use the large frets only):')
else:
    print(':')

for btn in buttons:
    print(btn)
    event = selected_dev.read_one()
    while event is None:
        time.sleep(0.05)
        event = selected_dev.read_one()
    bindings[btn] = event.code
    # flush events
    while event is not None:
        event = selected_dev.read_one()

rb_buttons = ['Green 2', 'Red 2', 'Yellow 2', 'Blue 2', 'Orange 2']

if is_rockband:
    print('Now hit the following small fret buttons:')

    for btn in rb_buttons:
        print(btn)
        event = selected_dev.read_one()
        while event is None:
            time.sleep(0.05)
            event = selected_dev.read_one()
        bindings[btn] = event.code
        # flush events
        while event is not None:
            event = selected_dev.read_one()

print('Available output devices:')
outputs = mido.get_output_names()
for i in range(len(outputs)):
    print(f'{i}: {outputs[i]}')

outindex = int(input('Enter the number of the device you want to use'))
if outindex < 0 or outindex >= len(devices):
    print('Error: device number was incorrect')
    exit()

selected_out = outputs[outindex]

custom_midi = input('Would you like to configure which buttons are bound to which MIDI instruments? If not, the default T-8 setup will be used. [y/n]').lower().startswith('y')

if not custom_midi:
    midi_config = {
        'Open': 36,
        'Green': 36,
        'Red': 38,
        'Yellow': 42,
        'Blue': 46,
        'Orange': 50
    }
    midi_channel = 10
    
else:
    midi_config = {}
    print('Please consult your device\'s manual for the note numbers of each instrument, then enter them at the prompts below:')
    midi_config['Open'] = int(input('Open (no fret buttons held)'))
    for button in bindings.keys():
        if button.startswith('Strum'):
            continue
        midi_config[button] = int(input(button))
    midi_channel = int(input('Enter midi channel'))

# build config dict
cfg = {
    'controller': devpath,
    'buttons': bindings,
    'output': selected_out,
    'midi': midi_config,
    'channel': midi_channel
}

# write to JSON file
open('config.json', 'w').write(json.dumps(cfg))

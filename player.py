import os
import pygame
import pygame.midi
from time import sleep
import evdev
from evdev import InputDevice, categorize, ecodes, KeyEvent

from noisterous.instrument import Instrument


def main():
    pygame.init()
    output = Instrument()
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    if devices:
        for device in devices:
            print(device.path, device.name, device.phys)
        dev = evdev.InputDevice(devices[0].path)

    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            keyevent = categorize(event)
            # TONE BUTTONS
            if "BTN_X" in keyevent.keycode:
                output.set_tone(1, keyevent.keystate)
            elif "BTN_Y" in keyevent.keycode:
                output.set_tone(2, keyevent.keystate)
            elif "BTN_A" in keyevent.keycode:
                output.set_tone(0, keyevent.keystate)
            elif "BTN_B" in keyevent.keycode:
                output.set_tone(2, keyevent.keystate)
            elif "BTN_TR" in keyevent.keycode:
                output.set_tone(3, keyevent.keystate)
            # PLAY BUTTON
            # elif "BTN_TL" in keyevent.keycode:
            #     if keyevent.keystate == KeyEvent.key_down:
            #         output.play(output.note)
            #     elif keyevent.keystate == KeyEvent.key_up:
            #         output.stop(output.note)
            elif "BTN_SELECT" in keyevent.keycode:
                output.reset()
            # ETC BUTTONS
            elif "BTN_MODE" in keyevent.keycode:
                break
            # else:
            #     print(keyevent)
        elif event.type == ecodes.EV_ABS:
            output.set_amplitude(event.code, event.value)


if __name__ == '__main__':
    main()

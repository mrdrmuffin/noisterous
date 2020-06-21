import os
import pygame
import pygame.midi
from time import sleep
import evdev
from evdev import InputDevice, categorize, ecodes, KeyEvent

INSTR_OCARINA = 80
INSTR_TRUMPET = 57
INSTR_PIANO = 0
INSTR_ORGAN = 19

NOTE_C3 = 48
NOTE_C4 = 60
NOTE_C5 = 72
NOTE_C6 = 84

MASK_A = [2, 4, 7, 1]
MASK_B = [1, 4, 7, 1]

LEFT_STICK_X = 0
LEFT_STICK_Y = 1
LEFT_TRIGGER = 2
RIGHT_TRIGGER = 5


class Instrument():
    def __init__(self):
        self._midi_init()
        self.note = NOTE_C4
        self.btns = [0, 0, 0, 0]
        self.is_playing = 0
        self.octave = NOTE_C4
        self.velocity = 127

    def __del__(self):
        del self.midi_out
        pygame.midi.quit()

    def reset(self):
        del self.midi_out
        pygame.midi.quit()
        self._midi_init()

    def _midi_init(self):
        pygame.midi.init()
        self.instrument = INSTR_TRUMPET
        port = 2
        for n in range(0, pygame.midi.get_count()):
            dev = pygame.midi.get_device_info(n)
            if dev[1] == b'TiMidity port 0':
                port = n
        # print ("Using output_id :%s:" % port)
        self.midi_out = pygame.midi.Output(port, 0)
        self.midi_out.set_instrument(self.instrument)

    def set_amplitude(self, code, value):
        if code == LEFT_STICK_X:
            if value < -18000:
                self.octave = NOTE_C3
            elif value > 18000:
                self.octave = NOTE_C5
            else:
                self.octave = NOTE_C4
            self.update_note(self.velocity)
        elif code == LEFT_TRIGGER:
            vol = int(127 * (value/1024))
            if vol > 0:
                self.midi_out.write_short(0xb0, 0x07, vol)
                if not self.is_playing:
                    self.play(self.note)
            else:
                self.stop(self.note)

    def set_tone(self, button, is_on):
        self.btns[button] = is_on
        self.update_note(self.velocity)

    def update_note(self, velocity):
        mask = MASK_B if self.btns[0] and self.btns[1] else MASK_A
        note = self.octave + sum(x * y for x, y in zip(mask, self.btns))
        if note != self.note or velocity != self.velocity:
            if self.is_playing:
                self.stop(self.note, self.velocity)
                self.play(note, velocity)
            self.note = note
            self.velocity = velocity

    def stop(self, note, velocity=127):
        self.is_playing = False
        self.midi_out.note_off(note, velocity)

    def play(self, note, velocity=127):
        self.is_playing = True
        # print(note)
        self.midi_out.note_on(note, velocity)

import threading
import time
from observable import *

def bpm_to_seconds_per_beat(bpm):
    minutes_per_beat = 1.0 / bpm
    return minutes_per_beat * 60.0

class SequencerModel(object):

    def __init__(self, number_samples, number_beats, bpm):
        self.number_samples = number_samples
        self.buttons = [[False for sample in range(number_samples)] for beat in range(number_beats)]
        self.playback_state = False
        self.bpm = bpm
        self.number_beats = number_beats
        self.current_beat = Observable(0)

    def toggle_button(self, position):
        beat, sample = position
        button_state = self.buttons[beat][sample]
        self.buttons[beat][sample] = not button_state
        return self.buttons[beat][sample]

    def toggle_playback(self):
        self.playback_state = not self.playback_state
        if (self.playback_state):
            self.start_playback()
        return self.playback_state

    def start_playback(self):
        t = threading.Thread(target=self.step_worker)
        self.current_beat.notify()
        t.start()

    def step_worker(self):
        while(self.playback_state):
            current_beat_value = self.current_beat.get_value()
            seconds_per_beat = bpm_to_seconds_per_beat(self.bpm)
            time.sleep(seconds_per_beat)
            if (self.playback_state): # check to see if playback stopped while sleeping
                if (current_beat_value >= self.number_beats - 1):
                    self.current_beat.set_value(0)
                else:
                    self.current_beat.set_value(current_beat_value + 1)

    def get_sample_states_for_beat(self, beat):
        return self.buttons[beat]

    def set_bpm(self, bpm):
        self.bpm = bpm

    def set_number_beats(self, new_number_beats):
        if new_number_beats - 1 < self.current_beat.get_value():
            self.current_beat.set_value(0)
        diff = new_number_beats - self.number_beats
        if diff > 0:
            for i in range(diff):
                self.buttons.append([False for sample in range(self.number_samples)])
        else:
            self.buttons = self.buttons[:new_number_beats]
        self.number_beats = new_number_beats
    
import threading
import time
from observable import *

# def bpm_to_seconds_per_beat(bpm):
#     # TODO error handling for 0.0 and negatives
#     minutes_per_beat = 1.0 / bpm
#     return minutes_per_beat * 60.0

class SequencerModel(object):

    def __init__(self, number_samples, number_beats, bpm):
        self.number_samples = number_samples
        self.buttons = [[False for sample in range(number_samples)] for beat in range(number_beats)]
        self.playback_state = False
        self.bpm = Observable(bpm)
        self.number_beats = Observable(number_beats)
        self.current_beat = Observable(0)

    def toggle_button(self, position):
        #TODO, out of bounds exception
        beat, sample = position
        button_state = self.buttons[beat][sample]
        self.buttons[beat][sample] = not button_state
        return self.buttons[beat][sample]

    def toggle_playback(self):
        self.playback_state = not self.playback_state
        return self.playback_state

    def set_bpm(self, bpm):
        #TODO error checking
        self.bpm.set_value(bpm)

    def set_number_beats(self, n_beats):
        self.number_beats.set_value(n_beats)

    def set_current_beat(self, current_beat):
        self.current_beat.set_value(current_beat)



    def step_worker(self):
        while(self.playback_on):
            print('current_beat ' + str(self.current_beat))
            self.audio.play_samples(self.grid[self.current_beat])
            seconds_per_beat = bpm_to_seconds_per_beat(self.bpm)
            time.sleep(seconds_per_beat)
            self.current_beat = self.current_beat + 1

    def set_playback(self, state):
        if (self.playback_on == state):
            return
        self.playback_on = state
        if (state):
            self.start_playback()

    def start_playback(self):
        t = threading.Thread(target=self.step_worker)
        t.start()
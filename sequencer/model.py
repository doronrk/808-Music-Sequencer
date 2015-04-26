import threading
import time
from observable import Observable

# utility function that converts beats per minute into seconds per beat
def bpm_to_seconds_per_beat(bpm):
    minutes_per_beat = 1.0 / bpm
    return minutes_per_beat * 60.0

class Model(object):
    """This class stores the state of the sequencer"""
    
    def __init__(self, number_samples, number_beats, bpm, swing, columns_per_beat):
        self.number_samples = number_samples
        # number of beats by number of samples list representing the state of each button 
        self.buttons = [[False for sample in range(number_samples)] for beat in range(number_beats)]
        self.playback_state = False
        self.bpm = bpm
        self.number_beats = number_beats
        # when current_beat %2 == 0, the beat duration increases proportionally by swing/3.0, otherwise, the beat duration decreases proportionally by swing/3.0
        self.set_swing(swing)
        # an int representing the number of columns visited for each beat
        self.columns_per_beat = columns_per_beat
        # current beat is observed by the controller to notify GUI and audio out 
        self.current_beat = Observable(0)

    def toggle_button(self, position):
        """Changes the state of the button at the position and returns the new state"""
        beat, sample = position
        button_state = self.buttons[beat][sample]
        self.buttons[beat][sample] = not button_state
        return self.buttons[beat][sample]

    def toggle_playback(self):
        """Changes whether playback is on and returns the new state"""
        self.playback_state = not self.playback_state
        if (self.playback_state):
            self._start_playback()
        return self.playback_state

    def _start_playback(self):
        t = threading.Thread(target=self._step_worker)
        self.current_beat.notify()
        t.start()

    def _step_worker(self):
        while(self.playback_state):
            seconds_for_this_beat = self._calculate_beat_duration()
            seconds_for_this_column = seconds_for_this_beat/self.columns_per_beat
            time.sleep(seconds_for_this_column)
            if (self.playback_state): # check to see if playback stopped while sleeping
                # wrap the beat back around to 0
                current_beat_value = self.current_beat.get_value()
                if (current_beat_value >= self.number_beats - 1):
                    self.current_beat.set_value(0)
                else:
                    self.current_beat.set_value(current_beat_value + 1)

    def _calculate_beat_duration(self):
        """
        This method returns the number of seconds this beat should last
        This value is calculatd by converting beats/minute to seconds/beat then applying swing
        """
        seconds_per_beat_before_swing = bpm_to_seconds_per_beat(self.bpm)
        swing_delta = (self.swing / 3.0) * seconds_per_beat_before_swing            
        current_beat_value = self.current_beat.get_value()
        if current_beat_value % 2 == 0:
            return seconds_per_beat_before_swing + swing_delta
        return seconds_per_beat_before_swing - swing_delta


    def get_sample_states_for_beat(self, beat):
        """Returns a list of the states of the buttons for the given beat"""
        return self.buttons[beat]

    def set_bpm(self, bpm):
        self.bpm = bpm

    def set_number_beats(self, new_number_beats):
        """
        Updates the number of beats.
        Maintains the state of unaffected buttons.
        State of new buttons defaults to off.
        """
        # resets current beat to 0 in the case that the current beat exceeds the new_number_beats
        if new_number_beats - 1 < self.current_beat.get_value():
            self.current_beat.set_value(0)
        diff = new_number_beats - self.number_beats
        # beats need to be added
        if diff > 0:
            for i in range(diff):
                self.buttons.append([False for sample in range(self.number_samples)])
        # beats need to be removed
        else:
            self.buttons = self.buttons[:new_number_beats]
        self.number_beats = new_number_beats

    def set_columns_per_beat(self, columns_per_beat):
        self.columns_per_beat = columns_per_beat

    def set_swing(self, swing):
        if swing < -1.0:
            self.swing = -1.0
        elif swing > 1.0:
            self.swing = 1.0
        else:
            self.swing = swing
    
from sequencer_model import *
import unittest
import time


class Tests(unittest.TestCase):

    def test_toggle(self):
        model = SequencerModel(8, 8, 120.0)
        result = model.toggle_button((0,0))
        self.assertTrue(result)
        self.assertTrue(model.buttons[0][0])

    def test_get_sample_states(self):
        model = SequencerModel(8, 8, 120.0)
        for sample in range(4, 8):
            model.toggle_button((3, sample))
        states = model.get_sample_states_for_beat(3)
        self.assertEquals(set([False]), set(states[0:4]))
        self.assertEquals(set([True]), set(states[4:]))
        states = model.get_sample_states_for_beat(0)
        self.assertEquals(set([False]), set(states))

    def test_set_number_beats_increase(self):
        model = SequencerModel(8, 8, 120.0)
        model.set_number_beats(10)
        self.assertTrue(model.number_beats == 10)
        for beat in range(10):
            for sample in range(8):
                position = (beat, sample)
                self.assertFalse(model.buttons[beat][sample])

    def test_set_number_beats_decrease(self):
        model = SequencerModel(8, 8, 120.0)
        model.set_number_beats(4)
        self.assertTrue(model.number_beats == 4)
        for beat in range(4):
            for sample in range(8):
                position = (beat, sample)
                self.assertFalse(model.buttons[beat][sample])

    def test_set_number_beats_keep_button_states(self):
        model = SequencerModel(8, 8, 120.0)
        for sample in range(4, 8):
            model.toggle_button((3, sample))
        model.set_number_beats(10)
        states = model.get_sample_states_for_beat(3)
        self.assertEquals(set([False]), set(states[0:4]))
        self.assertEquals(set([True]), set(states[4:]))

    def test_playback_constant_bpm(self):
        timing_tolerance = .1 # this is the propertion of one beat duration in which timing deviation is tolerated
        bpm = 500.0
        number_beats = 10.0
        seconds_per_beat = bpm_to_seconds_per_beat(bpm)
        timing_tolerance_in_seconds = timing_tolerance * seconds_per_beat
        total_elapsed_time = number_beats * seconds_per_beat
        print 'this playback test takes', total_elapsed_time, 'seconds'
        step_times = []
        def callback(value):
            step_times.append(time.time())
        model = SequencerModel(8, 8, bpm)
        model.current_beat.add_callback(callback)
        new_state = model.toggle_playback()
        self.assertTrue(new_state)

        time.sleep(total_elapsed_time + timing_tolerance_in_seconds)
        new_state = model.toggle_playback()
        self.assertFalse(new_state)

        for i in range(len(step_times) - 1):
            former = step_times[i]
            latter = step_times[i+1]
            elapsed_time = latter - former
            self.assertAlmostEqual(elapsed_time, seconds_per_beat, delta=timing_tolerance_in_seconds)

    def test_playback_change_bpm(self):
        begin = time.time()
        timing_tolerance_in_seconds = .01 
        bpm = 300.0
        first_seconds_per_beat = bpm_to_seconds_per_beat(bpm)
        total_time = first_seconds_per_beat * 3.5
        print 'this playback test takes', total_time
        step_times = []
        def callback(value):
            step_times.append(time.time())
        model = SequencerModel(8, 8, bpm)
        model.current_beat.add_callback(callback)
        model.toggle_playback()
        time.sleep(first_seconds_per_beat * 2 - .01)
        new_bpm = bpm * 2.0
        model.set_bpm(new_bpm)
        second_seconds_per_beat = bpm_to_seconds_per_beat(new_bpm)
        time.sleep(second_seconds_per_beat * 3 + .01)
        model.toggle_playback()

        before_change = step_times[0:3]
        after_change = step_times[2:]

        for i in range(len(before_change) - 1):
            former = before_change[i]
            latter = before_change[i+1]
            elapsed_time = latter - former
            self.assertAlmostEqual(elapsed_time, first_seconds_per_beat, delta=timing_tolerance_in_seconds)

        for i in range(len(after_change) - 1):
            former = after_change[i]
            latter = after_change[i+1]
            elapsed_time = latter - former
            self.assertAlmostEqual(elapsed_time, second_seconds_per_beat, delta=timing_tolerance_in_seconds)



if __name__ == '__main__':
    unittest.main()
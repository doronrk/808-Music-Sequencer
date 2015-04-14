from sequencer_model import *
import unittest
import time


class Tests(unittest.TestCase):

    def test_toggle(self):
        model = SequencerModel(8, 8, 120.0)
        result = model.toggle_button((0,0))
        self.assertTrue(result)
        self.assertTrue(model.buttons[0][0])

    def test_playback(self):
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





if __name__ == '__main__':
    unittest.main()
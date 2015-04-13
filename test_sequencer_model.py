from sequencer_model import *
import unittest

class Tests(unittest.TestCase):

    def test_init_get(self):
        sm = SequencerModel(4, 8, 60.0)
        self.assertTrue(sm.number_samples == 4)
        self.assertTrue(sm.number_beats.get_value() == 8)
        self.assertTrue(sm.bpm.get_value() == 60.0)
        self.assertTrue(sm.current_beat.get_value() == 0)
        self.assertTrue(sm.playback_on.get_value() == False)


    # TODO move to controller tests
    # def test_bpm_conversion_valid(self):
    #     self.assertTrue(bpm_to_seconds_per_beat(60.0) == 1.0)
    #     self.assertTrue(bpm_to_seconds_per_beat(120.0) == 0.5)
    #     self.assertTrue(bpm_to_seconds_per_beat(90.0) == .66667)

    # def test_bpm_conversion_invalid(self):
    #     #TODO implement
    #     self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
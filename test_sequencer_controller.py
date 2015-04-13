from sequencer_controller import *
import unittest

class Tests(unittest.TestCase):

    def test_sample_folder(self):
        sc = SequencerController('samples')

if __name__ == '__main__':
    unittest.main()
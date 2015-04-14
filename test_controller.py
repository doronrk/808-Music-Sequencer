from sequencer_controller import *
import unittest

def create_controller():
    root = Tkinter.Tk()
    sample_files = ['file/0.wav', 'file/1.wav', 'file/2.wav']
    controller = SequencerController(root, sample_files, False)
    return controller

class Tests(unittest.TestCase):

    class PseudoEvent(object):
        def __init__(self, position):
            self.widget = Tests.PseudoWidget()
            self.widget.position = position

    class PseudoWidget(object):
        def __init__(self):
            pass

    def test_sequencer_click(self):
        controller = create_controller()
        e0 = Tests.PseudoEvent((0,0))
        e1 = Tests.PseudoEvent((0,1))
        e2 = Tests.PseudoEvent((0,2))
        controller.sequencer_click_handler(e0)
        self.assertTrue(controller.sequencer_model.buttons[0][0])
        controller.sequencer_click_handler(e0)
        self.assertFalse(controller.sequencer_model.buttons[0][0])
        controller.sequencer_click_handler(e1)
        controller.sequencer_click_handler(e2)
        self.assertTrue(controller.sequencer_model.buttons[0][1])
        self.assertTrue(controller.sequencer_model.buttons[0][2])





if __name__ == '__main__':
    unittest.main()
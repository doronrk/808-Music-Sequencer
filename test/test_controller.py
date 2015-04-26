from sequencer.controller import Controller, DEFAULT_N_BEATS, DEFAULT_BPM
import unittest
import Tkinter

def create_controller():
    root = Tkinter.Tk()
    sample_files = ['file/0.wav', 'file/1.wav', 'file/2.wav']
    controller = Controller(root, sample_files, False)
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
        self.assertTrue(controller.model.buttons[0][0])
        controller.sequencer_click_handler(e0)
        self.assertFalse(controller.model.buttons[0][0])
        controller.sequencer_click_handler(e1)
        controller.sequencer_click_handler(e2)
        self.assertTrue(controller.model.buttons[0][1])
        self.assertTrue(controller.model.buttons[0][2])

        self.assertFalse(controller.editor.button_grid.buttons[0][0].state)
        self.assertTrue(controller.editor.button_grid.buttons[0][1].state)
        self.assertTrue(controller.editor.button_grid.buttons[0][2].state)
    
    def test_playback_click(self):
        controller = create_controller()
        e0 = Tests.PseudoEvent((0,0))
        controller.playback_click_handler(e0)
        self.assertTrue(controller.model.playback_state)
        self.assertTrue(controller.editor.transport_bar.playback_button.state)

        controller.playback_click_handler(e0)
        self.assertFalse(controller.model.playback_state)
        self.assertFalse(controller.editor.transport_bar.playback_button.state)

    def test_bpm_setter_invalid_bpm(self):
        controller = create_controller()
        e0 = Tests.PseudoEvent((0,0))
        controller.editor.transport_bar.bpm.entry.insert(0, 'not a number')
        controller.bpm_setter_click_handler(e0)
        self.assertTrue(controller.model.bpm == DEFAULT_BPM)

        controller.editor.transport_bar.bpm.entry.insert(0, '0.0')
        controller.bpm_setter_click_handler(e0)
        self.assertTrue(controller.model.bpm == DEFAULT_BPM)

        controller.editor.transport_bar.bpm.entry.insert(0, '-1.0')
        controller.bpm_setter_click_handler(e0)
        self.assertTrue(controller.model.bpm == DEFAULT_BPM)

    def test_number_beats_setter_invalid_bpm(self):
        controller = create_controller()
        e0 = Tests.PseudoEvent((0,0))
        controller.editor.transport_bar.number_beats.entry.insert(0, 'not a number')
        controller.number_beats_setter_click_handler(e0)
        self.assertTrue(controller.model.number_beats == DEFAULT_N_BEATS)

        controller.editor.transport_bar.number_beats.entry.insert(0, '3.5')
        controller.number_beats_setter_click_handler(e0)
        self.assertTrue(controller.model.number_beats == DEFAULT_N_BEATS)

        controller.editor.transport_bar.number_beats.entry.insert(0, '0.0')
        controller.number_beats_setter_click_handler(e0)
        self.assertTrue(controller.model.number_beats == DEFAULT_N_BEATS)

        controller.editor.transport_bar.number_beats.entry.insert(0, '-1.0')
        controller.number_beats_setter_click_handler(e0)
        self.assertTrue(controller.model.number_beats == DEFAULT_N_BEATS)

    def test_beat_update_handler(self):
        controller = create_controller()
        controller.beat_update_handler(0)
        header_elements = controller.editor.header.header_elements
        self.assertTrue(header_elements[0].state)
        self.assertEquals(set([False]), set([element.state for element in header_elements[1:]]))
        controller.beat_update_handler(3)
        self.assertTrue(header_elements[3].state)
        self.assertEquals(set([False]), set([element.state for element in header_elements[:3]]))
        self.assertEquals(set([False]), set([element.state for element in header_elements[4:]]))

    def test_swing_scale(self):
        controller = create_controller()
        new_swing = .2
        controller.editor.transport_bar.swing.set(new_swing)
        controller.swing_setter_click_handler(None)
        self.assertAlmostEquals(new_swing, controller.model.swing)


if __name__ == '__main__':
    unittest.main()
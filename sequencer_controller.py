import sys
import threading
import time
from os import listdir
from sequencer_model import *
from sequencer_editor import *
from sequencer_audio import *

class SequencerController(object):

    DEFAULT_N_BEATS = 8
    DEFAULT_BPM = 60.0

    def __init__(self, root, sample_folder_path):
        path_directory = listdir(sample_folder_path)
        number_samples = len(path_directory)
        self.sequencer_model = SequencerModel(number_samples, SequencerController.DEFAULT_N_BEATS, SequencerController.DEFAULT_BPM)
        self.sequencer_model.current_beat.add_callback(self.beat_update_handler)

        self.sequencer_editor = SequencerEditor(root, SequencerController.DEFAULT_N_BEATS, number_samples)
        self.sequencer_editor.button_grid.bind("<Button-1>", self.sequencer_click_handler)
        self.sequencer_editor.transport_bar.playback_button.bind("<Button-1>", self.playback_click_handler)

        self.sequencer_audio = SequencerAudio(path_directory)

    def sequencer_click_handler(self, event):
        position = event.widget.position
        new_state = self.sequencer_model.toggle_button(position)
        self.sequencer_editor.set_button_state(position, new_state)

    def playback_click_handler(self, event):
        playback_state = self.sequencer_model.toggle_playback()
        self.sequencer_editor.set_playback_state(playback_state)

    def beat_update_handler(self, current_beat):
        self.sequencer_editor.set_current_beat(current_beat)
        sample_states = self.sequencer_model.get_sample_states_for_beat(current_beat)
        self.sequencer_audio.play_samples(sample_states)


if __name__ == "__main__":
    sample_folder_path = sys.argv[1]
    root = Tkinter.Tk()
    root.withdraw()
    app = SequencerController(root, sample_folder_path)
    root.title("Sequencer")
    #root.resizable(height=True, width=True)
    root.mainloop()
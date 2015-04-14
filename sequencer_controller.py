import sys
import threading
import time
from os import listdir
from sequencer_model import *
from sequencer_editor import *
from sequencer_audio import *

class SequencerController(object):

    DEFAULT_N_BEATS = 8
    DEFAULT_BPM = 135.0

    def __init__(self, root, sample_files):
        self.sequencer_model = SequencerModel(len(sample_files), SequencerController.DEFAULT_N_BEATS, SequencerController.DEFAULT_BPM)
        self.sequencer_model.current_beat.add_callback(self.beat_update_handler)

        sample_names = [sample_file[:-4].split('/', 1)[1] for sample_file in sample_files]
        self.sequencer_editor = SequencerEditor(root, SequencerController.DEFAULT_N_BEATS, sample_names)
        self.sequencer_editor.button_grid.bind("<Button-1>", self.sequencer_click_handler)
        self.sequencer_editor.transport_bar.playback_button.bind("<Button-1>", self.playback_click_handler)
        self.sequencer_editor.sample_boxes.bind("<Button-1>", self.sample_box_click_handler)
        
        self.sequencer_audio = SequencerAudio(sample_files)

    def sequencer_click_handler(self, event):
        position = event.widget.position
        new_state = self.sequencer_model.toggle_button(position)
        self.sequencer_editor.set_button_state(position, new_state)

    def playback_click_handler(self, event):
        playback_state = self.sequencer_model.toggle_playback()
        self.sequencer_editor.set_playback_state(playback_state)

    def sample_box_click_handler(self, event):
        sample_number = event.widget.sample_number
        self.sequencer_audio.play_sample(sample_number)

    def beat_update_handler(self, current_beat):
        self.sequencer_editor.set_current_beat(current_beat)
        sample_states = self.sequencer_model.get_sample_states_for_beat(current_beat)
        self.sequencer_audio.play_samples(sample_states)


if __name__ == "__main__":
    sample_folder_path = sys.argv[1]
    files_in_sample_folder = listdir(sample_folder_path)
    wav_files_in_sample_folder = [sample_folder_path + '/' + sample for sample in files_in_sample_folder if sample[-4:] == '.wav']
    root = Tkinter.Tk()
    root.withdraw()
    app = SequencerController(root, wav_files_in_sample_folder)
    root.title("Sequencer")
    root.mainloop()
import sys
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
        
        self.sequencer_editor = SequencerEditor(root, SequencerController.DEFAULT_N_BEATS, number_samples)
        self.sequencer_editor.button_grid.bind("<Button-1>", self.sequencer_click_handler)
        #self.sequencer_audio = SequencerAudio()


    def sequencer_click_handler(self, event):
        position = event.widget.position
        new_state = self.sequencer_model.toggle_button(position)
        self.sequencer_editor.set_button_state(position, new_state)

if __name__ == "__main__":
    sample_folder_path = sys.argv[1]
    root = Tkinter.Tk()
    root.withdraw()
    app = SequencerController(root, sample_folder_path)
    root.title("Sequencer")
    #root.resizable(height=True, width=True)
    root.mainloop()
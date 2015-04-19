import sys
import threading
from os import listdir
from sequencer_model import *
from sequencer_editor import *
from sequencer_console_output import *

DEFAULT_N_BEATS = 8
DEFAULT_BPM = 135.0
DEFAULT_SWING = 0.0

class SequencerController(object):
    """The SequencerController updates the SequencerModel according to GUI events
    and updates Audio/Console output and the GUI when the current beat changes
    """

    def __init__(self, root, sample_files, using_audio_out):
        """
        root - main GUI window
        sample_files - list of relative paths to samples
        using_audio_out - True if pygame dependency supported, False otherwise
        """
        
        self.sequencer_model = SequencerModel(len(sample_files), DEFAULT_N_BEATS, DEFAULT_BPM, DEFAULT_SWING)
        self.sequencer_model.current_beat.add_callback(self.beat_update_handler)

        # remove relative path and .wav from filenames
        sample_names = [sample_file[:-4].split('/', 1)[1] for sample_file in sample_files]
        self.sequencer_editor = SequencerEditor(root, DEFAULT_N_BEATS, sample_names, DEFAULT_BPM, DEFAULT_SWING)
        # binds callbacks with corresponding GUI elements 
        self.sequencer_editor.button_grid.bind("<Button-1>", self.sequencer_click_handler)
        self.sequencer_editor.transport_bar.playback_button.bind("<Button-1>", self.playback_click_handler)
        self.sequencer_editor.transport_bar.bpm.bind("<Button-1>", self.bpm_setter_click_handler)
        self.sequencer_editor.transport_bar.number_beats.bind("<Button-1>", self.number_beats_setter_click_handler)
        self.sequencer_editor.transport_bar.swing.bind("<ButtonRelease-1>", self.swing_setter_click_handler)
        self.sequencer_editor.sample_boxes.bind("<Button-1>", self.sample_box_click_handler)
        # intializes audio output if dependencies available, console output otherwise
        self.sequencer_audio = SequencerAudio(sample_files) if using_audio_out else SequencerConsoleOutput(sample_names)

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

    def bpm_setter_click_handler(self, event):
        entry = self.sequencer_editor.transport_bar.bpm.get()
        new_bpm = None
        try:
            new_bpm = float(entry)
        except ValueError:
            return
        if (new_bpm <= 0.0):
            return
        self.sequencer_model.set_bpm(new_bpm)

    def number_beats_setter_click_handler(self, event):
        entry = self.sequencer_editor.transport_bar.number_beats.get()
        new_number_beats = None
        try:
            new_number_beats = int(entry)
        except ValueError:
            return
        if (new_number_beats < 1):
            return
        self.sequencer_model.set_number_beats(new_number_beats)
        self.sequencer_editor.set_number_beats(new_number_beats)

    def swing_setter_click_handler(self, event):
        value = self.sequencer_editor.transport_bar.swing.get()
        print value

    def beat_update_handler(self, current_beat):
        self.sequencer_editor.set_current_beat(current_beat)
        sample_states = self.sequencer_model.get_sample_states_for_beat(current_beat)
        self.sequencer_audio.play_samples(sample_states)


if __name__ == "__main__":
    if not len(sys.argv) == 2:
        print 'usage: python sequencer_controller.py [relative_path_to_sample_folder]'
        sys.exit()
    sample_folder_path = sys.argv[1]
    try:
        files_in_sample_folder = listdir(sample_folder_path)
    except OSError:
        print 'Could not locate sample folder'
        sys.exit()
    wav_files_in_sample_folder = [sample_folder_path + '/' + sample for sample in files_in_sample_folder if sample[-4:] == '.wav']
    if len(wav_files_in_sample_folder) == 0:
        print 'Could not locate any .wav files in the sample folder'
        sys.exit()

    using_audio_out = True
    try:
        from sequencer_audio import *
        print 'Pygame audio supported, outputting samples to audio out'
    except ImportError:
        using_audio_out = False
        #from sequencer_console_output import *
        print 'Pygame audio not supported, outputting sample names to console'
        print 'Please install Pygame for audio out'

    root = Tkinter.Tk()
    root.withdraw()
    app = SequencerController(root, wav_files_in_sample_folder, using_audio_out)
    root.title("Sequencer")
    root.mainloop()
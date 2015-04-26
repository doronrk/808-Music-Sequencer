import threading
from model import Model
from editor import Editor

DEFAULT_N_BEATS = 8
DEFAULT_BPM = 135.0
DEFAULT_SWING = 0.0
DEFAULT_COLUMNS_PER_BEAT = 2.0

class Controller(object):
    """The SequencerController updates the SequencerModel according to GUI events
    and updates Audio/Console output and the GUI when the current beat changes
    """

    def __init__(self, root, sample_files, using_audio_out):
        """
        root - main GUI window
        sample_files - list of relative paths to samples
        using_audio_out - True if pygame dependency supported, False otherwise
        """
        self.root = root
        self.model = Model(len(sample_files), DEFAULT_N_BEATS, DEFAULT_BPM, DEFAULT_SWING, DEFAULT_COLUMNS_PER_BEAT)
        self.model.current_beat.add_callback(self.beat_update_handler)

        # remove relative path and .wav from filenames
        sample_names = [sample_file[:-4].rsplit('/', 1)[1] for sample_file in sample_files]
        self.editor = Editor(root, DEFAULT_N_BEATS, sample_names, DEFAULT_BPM, DEFAULT_SWING)
        # handle window close
        self.editor.protocol("WM_DELETE_WINDOW", self.quit)
        # binds callbacks with corresponding GUI elements 
        self.editor.quit_button.bind("<Button-1>", self.quit_click_handler)
        self.editor.button_grid.bind("<Button-1>", self.sequencer_click_handler)
        self.editor.transport_bar.playback_button.bind("<Button-1>", self.playback_click_handler)
        self.editor.transport_bar.bpm.bind("<Button-1>", self.bpm_setter_click_handler)
        self.editor.transport_bar.number_beats.bind("<Button-1>", self.number_beats_setter_click_handler)
        self.editor.transport_bar.swing.bind("<ButtonRelease-1>", self.swing_setter_click_handler)
        self.editor.sample_boxes.bind("<Button-1>", self.sample_box_click_handler)
        # intializes audio output if dependencies available, console output otherwise
        if using_audio_out:
            from audio import Audio
            self.output = Audio(sample_files)
        else:
            from console_output import ConsoleOutput
            self.output = ConsoleOutput(sample_names)

    def quit(self):
        self.model.playback_state = False
        self.editor.destroy()
        self.root.quit()

    def quit_click_handler(self, event):
        self.quit()

    def sequencer_click_handler(self, event):
        position = event.widget.position
        new_state = self.model.toggle_button(position)
        self.editor.set_button_state(position, new_state)

    def playback_click_handler(self, event):
        playback_state = self.model.toggle_playback()
        self.editor.set_playback_state(playback_state)

    def sample_box_click_handler(self, event):
        sample_number = event.widget.sample_number
        self.output.play_sample(sample_number)

    def bpm_setter_click_handler(self, event):
        entry = self.editor.transport_bar.bpm.get()
        new_bpm = None
        try:
            new_bpm = float(entry)
        except ValueError:
            return
        if (new_bpm <= 0.0):
            return
        self.model.set_bpm(new_bpm)

    def number_beats_setter_click_handler(self, event):
        entry = self.editor.transport_bar.number_beats.get()
        new_number_beats = None
        try:
            new_number_beats = int(entry)
        except ValueError:
            return
        if (new_number_beats < 1):
            return
        self.model.set_number_beats(new_number_beats)
        self.editor.set_number_beats(new_number_beats)

    def swing_setter_click_handler(self, event):
        value = float(self.editor.transport_bar.swing.get())
        self.model.set_swing(value)

    def beat_update_handler(self, current_beat):
        self.editor.set_current_beat(current_beat)
        sample_states = self.model.get_sample_states_for_beat(current_beat)
        self.output.play_samples(sample_states)
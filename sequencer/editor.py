import Tkinter

DEFAULT_NOTE_DIMENSION = 75
DEFAULT_TRANSPORT_DIMENSION = DEFAULT_NOTE_DIMENSION / 2.0
OFFSET_DISTANCE = DEFAULT_NOTE_DIMENSION / 10.0
BUTTON_TEXT_FONT_SIZE = 8

class Editor(Tkinter.Toplevel):
    """This is the GUI and propages click events to the SequencerController
    It consists of
        Transport Bar-  Allows the user to control the playback, bpm, and number of beats
        Header-         Indicates the current beat
        Sample Boxes-   Indicates the name of each sample. Clicking one triggers a preview of the sample
        Button Grid-    Indicates the state of each button. Clicking a button toggles its state
    """

    def __init__(self, root, number_beats, sample_names, bpm, swing):
        Tkinter.Toplevel.__init__(self, root)
        self.root = root

        number_samples = len(sample_names)
        
        # handle exit
        self.quit_button = Tkinter.Button(self, text="Quit")
        self.quit_button.grid(row=0, column=0, padx=1, pady=1)

        self.transport_bar = TransportBar(self, bpm, number_beats, swing)
        self.transport_bar.grid(row=1, column=1,padx=1, pady=1)

        self.header = Header(self, number_beats)
        self.header.grid(row=2, column=1, padx=1, pady=1)

        self.sample_boxes = SampleBoxes(self, sample_names)
        self.sample_boxes.grid(row=3, column=0, padx=1, pady=1)

        self.button_grid = ButtonGrid(self, number_beats, number_samples)
        self.button_grid.grid(row=3, column=1, padx=1, pady=1)

    def set_button_state(self, position, state):
        beat, sample = position
        self.button_grid.buttons[beat][sample].set_state(state)

    def set_current_beat(self, current_beat):
        self.header.set_current_beat(current_beat)

    def set_playback_state(self, state):
        self.transport_bar.playback_button.set_state(state)

    def set_number_beats(self, new_number_beats):
        self.header.set_number_beats(new_number_beats)
        self.button_grid.set_number_beats(new_number_beats)
        self.number_beats = new_number_beats

class TransportBar(Tkinter.Frame):
    """Allows the user to control the playback, bpm, and number of beats"""
    def __init__(self, master, bpm, number_beats, swing):
        Tkinter.Frame.__init__(self, master)
        self.playback_button = PlaybackButton(self)
        self.playback_button.grid(row=0, column=0, padx=1, pady=1)

        self.bpm = EntrySetterPair(self, str(bpm), "set bpm")
        self.bpm.grid(row=0, column=1, padx=1, pady=1)
        self.number_beats = EntrySetterPair(self, str(number_beats), "set beats")
        self.number_beats.grid(row=0, column=2, padx=1, pady=1)
        self.swing = Tkinter.Scale(master, from_=-1.0, to=1.0, orient=Tkinter.HORIZONTAL, label="swing", resolution=0.01)
        self.swing.set(swing)
        self.swing.grid(row=0, column=3, padx=1, pady=1)

class EntrySetterPair(Tkinter.Frame):
    """Wraps a text entry widget and its corresponding setter button"""
    def __init__(self, master, initial_value, setter_text):
        Tkinter.Frame.__init__(self, master)
        self.entry = Tkinter.Entry(self, width=5)
        self.entry.grid(row=0, column=0, padx=1, pady=1)
        self.entry.insert(0, initial_value)
        self.setter = Tkinter.Canvas(self, width=DEFAULT_TRANSPORT_DIMENSION, 
                                      height=DEFAULT_TRANSPORT_DIMENSION, highlightthickness=1, 
                                      highlightbackground="black")
        self.setter.create_text((DEFAULT_TRANSPORT_DIMENSION/2.0,DEFAULT_TRANSPORT_DIMENSION/2.0), text=setter_text,  font=("Helvetica",BUTTON_TEXT_FONT_SIZE))
        self.setter.grid(row=0, column=1, padx=1, pady=1)
        # propagate click events from the setter, not the entry box
        self.setter.bindtags(self)

    def get(self):
        return self.entry.get()

class PlaybackButton(Tkinter.Canvas):
    STOP_COLOR = 'red'
    START_COLOR = 'green'

    def __init__(self, master):
        Tkinter.Canvas.__init__(self, master, width=DEFAULT_TRANSPORT_DIMENSION, height=DEFAULT_TRANSPORT_DIMENSION
                                , highlightthickness=1, highlightbackground="black")
        # coordinates for the stop playback shape
        self.rect_coords = (OFFSET_DISTANCE, OFFSET_DISTANCE,
                            DEFAULT_TRANSPORT_DIMENSION - OFFSET_DISTANCE, DEFAULT_TRANSPORT_DIMENSION - OFFSET_DISTANCE)
        # coordinates for the start playback shape
        self.tri_coords = (OFFSET_DISTANCE, OFFSET_DISTANCE, 
                           OFFSET_DISTANCE, DEFAULT_TRANSPORT_DIMENSION - OFFSET_DISTANCE,
                           DEFAULT_TRANSPORT_DIMENSION - OFFSET_DISTANCE, DEFAULT_TRANSPORT_DIMENSION/2.0)
        self.set_state(False)

    def set_state(self, state):
        self.state = state
        self.redraw()

    def redraw(self):
        self.delete("all")
        if self.state:
            self.create_rectangle(self.rect_coords, fill=PlaybackButton.STOP_COLOR)
        else:
            self.create_polygon(self.tri_coords, fill=PlaybackButton.START_COLOR)

class Header(Tkinter.Frame):
    """A series of rectangles indicating the current beat"""
    def __init__(self, master, number_beats):
        Tkinter.Frame.__init__(self, master)
        self.number_beats = 0
        self.header_elements = []
        self.set_number_beats(number_beats)

    def set_number_beats(self, new_number_beats):
        diff = new_number_beats - self.number_beats
        # elements need to be added
        if diff > 0:
            for beat in range(self.number_beats, self.number_beats + diff):
                header_element = TwoColorBox(self, height=5)
                header_element.grid(row=0, column=beat, padx=1, pady=1)
                self.header_elements.append(header_element)
        # elements need to be removed
        else:
            for header_element in self.header_elements[new_number_beats:]:
                header_element.grid_forget()
            self.header_elements = self.header_elements[:new_number_beats]
        self.number_beats = new_number_beats

    def set_current_beat(self, current_beat):
        """highlights the current beat, unhighlights the others"""
        for beat, header_element in enumerate(self.header_elements):
            if (beat == current_beat):
                header_element.set_state(True)
            else:
                header_element.set_state(False) 

class SampleBoxes(Tkinter.Frame):
    """Indicates the name of each sample. Clicking one triggers a preview of the sample"""
    def __init__(self, master, sample_names):
        Tkinter.Frame.__init__(self, master)
        for n, sample_name in enumerate(sample_names):
            sample_box = Tkinter.Canvas(self, width=DEFAULT_NOTE_DIMENSION, height=DEFAULT_NOTE_DIMENSION)
            sample_box.create_text((DEFAULT_NOTE_DIMENSION/2.0,DEFAULT_NOTE_DIMENSION/2.0), text=sample_name)
            sample_box.grid(row=n, column=0, padx=1, pady=1)
            sample_box.sample_number = n
            # propagate click events to SampleBoxes instead of default TopLevel 
            sample_box.bindtags((self))

class ButtonGrid(Tkinter.Frame):
    """Indicates the state of each button. Clicking a button toggles its state"""
    def __init__(self, master, number_beats, number_samples):
        Tkinter.Frame.__init__(self, master)
        self.number_samples = number_samples
        self.buttons = []
        self.number_beats = 0
        self.set_number_beats(number_beats)

    def set_number_beats(self, new_number_beats):
        diff = new_number_beats - self.number_beats
        # columns need to be added
        if diff > 0:
            for beat in range(self.number_beats, self.number_beats + diff):
                button_column = []
                for sample in range(self.number_samples):
                    button = TwoColorBox(self)
                    button.grid(row=sample, column=beat, padx=1, pady=1)
                    button.position = (beat, sample)
                    # propagate click events to the ButtonGrid instead of default TopLevel 
                    button.bindtags((self))
                    button_column.append(button)
                self.buttons.append(button_column)
        # columns need to be removed
        else:
            for button_column in self.buttons[new_number_beats:]:
                for button in button_column:
                    button.grid_forget()
            self.buttons = self.buttons[:new_number_beats]
        self.number_beats = new_number_beats


class TwoColorBox(Tkinter.Canvas): 
    COLOR_EMPTY = "white"
    COLOR_FILLED = "gray50"

    def __init__(self, master, width=DEFAULT_NOTE_DIMENSION, height=DEFAULT_NOTE_DIMENSION):
        Tkinter.Canvas.__init__(self, master, width=width, height=height,
            background=TwoColorBox.COLOR_EMPTY, highlightthickness=1,
            highlightbackground="black")
        self.position = None
        self.set_state(False)

    def set_state(self, state):
        self.state = state
        self.redraw()

    def redraw(self):
        color = TwoColorBox.COLOR_FILLED if self.state else TwoColorBox.COLOR_EMPTY
        self.configure(background=color)



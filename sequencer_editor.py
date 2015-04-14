import Tkinter

DEFAULT_NOTE_DIMENSION = 100
DEFAULT_TRANSPORT_DIMENSION = DEFAULT_NOTE_DIMENSION / 2.0
OFFSET_DISTANCE = DEFAULT_NOTE_DIMENSION / 10.0


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

class ButtonGrid(Tkinter.Frame):

    def __init__(self, master, number_beats, number_samples):
        Tkinter.Frame.__init__(self, master)
        self.number_samples = number_samples
        self.buttons = []
        self.number_beats = 0
        self.set_number_beats(number_beats)

    def set_number_beats(self, new_number_beats):
        diff = new_number_beats - self.number_beats
        if diff > 0:
            for beat in range(self.number_beats, self.number_beats + diff):
                button_column = []
                for sample in range(self.number_samples):
                    button = TwoColorBox(self)
                    button.grid(row=sample, column=beat, padx=1, pady=1)
                    button.position = (beat, sample)
                    # propagate click events to the button grid instead of default TopLevel 
                    button.bindtags((self))
                    button_column.append(button)
                self.buttons.append(button_column)
        else:
            for button_column in self.buttons[new_number_beats:]:
                for button in button_column:
                    button.grid_forget()
            self.buttons = self.buttons[:new_number_beats]
        self.number_beats = new_number_beats

class Header(Tkinter.Frame):

    def __init__(self, master, number_beats):
        Tkinter.Frame.__init__(self, master)
        self.number_beats = 0
        self.header_elements = []
        self.set_number_beats(number_beats)

    def set_number_beats(self, new_number_beats):
        diff = new_number_beats - self.number_beats
        if diff > 0:
            for beat in range(self.number_beats, self.number_beats + diff):
                header_element = TwoColorBox(self, height=5)
                header_element.grid(row=0, column=beat, padx=1, pady=1)
                self.header_elements.append(header_element)
        else:
            for header_element in self.header_elements[new_number_beats:]:
                header_element.grid_forget()
            self.header_elements = self.header_elements[:new_number_beats]
        self.number_beats = new_number_beats

    def set_current_beat(self, current_beat):
        for beat, header_element in enumerate(self.header_elements):
            if (beat == current_beat):
                header_element.set_state(True)
            else:
                header_element.set_state(False) 

class PlaybackButton(Tkinter.Canvas):

    def __init__(self, master):
        Tkinter.Canvas.__init__(self, master, width=DEFAULT_TRANSPORT_DIMENSION, height=DEFAULT_TRANSPORT_DIMENSION
                                , highlightthickness=1, highlightbackground="black")
        self.rect_coords = (OFFSET_DISTANCE, OFFSET_DISTANCE,
                            DEFAULT_TRANSPORT_DIMENSION - OFFSET_DISTANCE, DEFAULT_TRANSPORT_DIMENSION - OFFSET_DISTANCE)
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
            self.create_rectangle(self.rect_coords, fill='red')
        else:
            self.create_polygon(self.tri_coords, fill='green')

class TransportBar(Tkinter.Frame):

    def __init__(self, master, bpm, number_beats):
        Tkinter.Frame.__init__(self, master)
        self.playback_button = PlaybackButton(self)
        self.playback_button.grid(row=0, column=0, padx=1, pady=1)

        self.bpm_entry = Tkinter.Entry(self)
        self.bpm_entry.grid(row=0, column=1, padx=1, pady=1)
        self.bpm_entry.insert(0, str(bpm))
        self.bpm_setter = Tkinter.Canvas(self, width=DEFAULT_TRANSPORT_DIMENSION, 
                                      height=DEFAULT_TRANSPORT_DIMENSION, highlightthickness=1, 
                                      highlightbackground="black")
        self.bpm_setter.create_text((DEFAULT_TRANSPORT_DIMENSION/2.0,DEFAULT_TRANSPORT_DIMENSION/2.0), text='set bpm',  font=("Helvetica",10))
        self.bpm_setter.grid(row=0, column=2, padx=1, pady=1)

        self.number_beats_entry = Tkinter.Entry(self)
        self.number_beats_entry.grid(row=0, column=3, padx=1, pady=1)
        self.number_beats_entry.insert(0, str(number_beats))
        self.number_beats_setter = Tkinter.Canvas(self, width=DEFAULT_TRANSPORT_DIMENSION, 
                                      height=DEFAULT_TRANSPORT_DIMENSION, highlightthickness=1, 
                                      highlightbackground="black")
        self.number_beats_setter.create_text((DEFAULT_TRANSPORT_DIMENSION/2.0,DEFAULT_TRANSPORT_DIMENSION/2.0), text='set beats',  font=("Helvetica",10))
        self.number_beats_setter.grid(row=0, column=4, padx=1, pady=1)


class SampleBoxes(Tkinter.Frame):

    def __init__(self, master, sample_names):
        Tkinter.Frame.__init__(self, master)
        for n, sample_name in enumerate(sample_names):
            sample_box = Tkinter.Canvas(self, width=DEFAULT_NOTE_DIMENSION, height=DEFAULT_NOTE_DIMENSION)
            sample_box.create_text((DEFAULT_NOTE_DIMENSION/2.0,DEFAULT_NOTE_DIMENSION/2.0), text=sample_name)
            sample_box.grid(row=n, column=0, padx=1, pady=1)
            sample_box.sample_number = n
            # propagate click events to the button grid instead of default TopLevel 
            sample_box.bindtags((self))

class SequencerEditor(Tkinter.Toplevel):

    def __init__(self, master, number_beats, sample_names, bpm):
        Tkinter.Toplevel.__init__(self, master)

        number_samples = len(sample_names)

        self.transport_bar = TransportBar(self, bpm, number_beats)
        self.transport_bar.grid(row=0, column=1,padx=1, pady=1)

        self.header = Header(self, number_beats)
        self.header.grid(row=1, column=1, padx=1, pady=1)

        self.sample_boxes = SampleBoxes(self, sample_names)
        self.sample_boxes.grid(row=2, column=0, padx=1, pady=1)

        self.button_grid = ButtonGrid(self, number_beats, number_samples)
        self.button_grid.grid(row=2, column=1, padx=1, pady=1)

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



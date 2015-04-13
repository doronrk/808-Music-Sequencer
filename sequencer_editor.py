import Tkinter

DEFAULT_SQAURE_DIMENSION = 100
OFFSET_DISTANCE = 10


class TwoColorBox(Tkinter.Canvas):

    COLOR_EMPTY = "white"
    COLOR_FILLED = "gray50"

    def __init__(self, master, width=DEFAULT_SQAURE_DIMENSION, height=DEFAULT_SQAURE_DIMENSION):
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
        self.buttons = []
        for beat in range(number_beats):
            button_column = []
            for sample in range(number_samples):
                button = TwoColorBox(self)
                button.grid(row=sample, column=beat, padx=1, pady=1)
                button.position = (beat, sample)
                # propagate click events to the button grid instead of default TopLevel 
                button.bindtags((self))
                button_column.append(button)
            self.buttons.append(button_column)


class Header(Tkinter.Frame):

    def __init__(self, master, number_beats):
        Tkinter.Frame.__init__(self, master)
        self.header_elements = []
        for beat in range(number_beats):
            header_element = TwoColorBox(self, height=5)
            header_element.grid(row=0, column=beat, padx=1, pady=1)
            self.header_elements.append(header_element)

class PlaybackButton(Tkinter.Canvas):

    def __init__(self, master):
        self.dimension = DEFAULT_SQAURE_DIMENSION/2.0
        Tkinter.Canvas.__init__(self, master, width=self.dimension, height=self.dimension
                                , highlightthickness=1, highlightbackground="black")
        self.rect_coords = (OFFSET_DISTANCE, OFFSET_DISTANCE,
                            self.dimension - OFFSET_DISTANCE, self.dimension - OFFSET_DISTANCE)
        self.tri_coords = (OFFSET_DISTANCE, OFFSET_DISTANCE, 
                           OFFSET_DISTANCE, self.dimension - OFFSET_DISTANCE,
                           self.dimension - OFFSET_DISTANCE, self.dimension/2.0)
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

    def __init__(self, master):
        Tkinter.Frame.__init__(self, master)
        self.playback_button = PlaybackButton(self)
        self.playback_button.grid()


class SequencerEditor(Tkinter.Toplevel):

    def __init__(self, master, number_beats, number_samples):
        Tkinter.Toplevel.__init__(self, master)

        self.transport_bar = TransportBar(self)
        self.transport_bar.grid(row=0, padx=1, pady=1)
        self.header = Header(self, number_beats)
        self.header.grid(row=1, padx=1, pady=1)

        self.button_grid = ButtonGrid(self, number_beats, number_samples)
        self.button_grid.grid(row=2, padx=1, pady=1)

    def set_button_state(self, position, state):
        beat, sample = position
        self.button_grid.buttons[beat][sample].set_state(state)

    def set_current_beat(self, current_beat):
        for beat, header_element in enumerate(self.header.header_elements):
            if (beat == current_beat):
                header_element.set_state(True)
            else:
                header_element.set_state(False) 

    def set_playback_state(self, state):
        self.transport_bar.playback_button.set_state(state)



class Observable(object):

    def __init__(self, initial_value=None):
        self.value = initial_value
        self.callbacks = []

    def add_callback(self, func):
        self.callbacks.append(func)

    def set_value(self, new_value):
        self.value = new_value
        self._do_callbacks()

    def _do_callbacks(self):
        for callback in self.callbacks:
            callback(self.value)

    def get_value(self):
        return self.value
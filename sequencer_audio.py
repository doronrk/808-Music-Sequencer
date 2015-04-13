class Audio(object):

    def __init__(self):
        self.samples = []

    def play_samples(self, sample_states):
        assert(len(self.samples) == len(sample_states))
        for sample, sample_state in zip(self.samples, sample_states):
            if sample_state:
                print '\t' + sample

    def add_sample(self, path):
        self.samples.append(path)

    def remove_sample(self, sample_number):
        #TODO error checking
        self.samples.pop(sample_number)
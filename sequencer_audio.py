class SequencerAudio(object):

    def __init__(self, sample_file_names):
        print sample_file_names
        self.samples = sample_file_names

    def play_samples(self, sample_states):
        for sample, sample_state in zip(self.samples, sample_states):
            if sample_state:
                print '\t' + sample

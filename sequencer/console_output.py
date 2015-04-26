class ConsoleOutput(object):

    def __init__(self, sample_files):
        """Outputs sample names to the console"""
        self.samples = sample_files

    def play_samples(self, sample_states):
        """Outputs the sample names with corresponding index == True in sample_states"""
        for sample, sample_state in zip(self.samples, sample_states):
            if sample_state:
                print(sample),
        print ''

    def play_sample(self, sample_number):
        print self.samples[sample_number]
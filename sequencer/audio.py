import pygame

class Audio(object):

    def __init__(self, sample_files):
        """Outputs samples to port audio"""
        # sets sampling rate, and buffer size to reduce latency
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()
        # load samples
        self.samples = [pygame.mixer.Sound(filename) for filename in sample_files]

    def play_samples(self, sample_states):
        """Plays samples with corresponding index == True in sample_states"""
        for sample, sample_state in zip(self.samples, sample_states):
            if sample_state:
                sample.play()

    def play_sample(self, sample_number):
        """Plays sample at index sample_number"""
        self.samples[sample_number].play()
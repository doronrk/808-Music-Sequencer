import pygame

class SequencerAudio(object):

    def __init__(self, sample_files):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        self.samples = [pygame.mixer.Sound(filename) for filename in sample_files]

    def play_samples(self, sample_states):
        for sample, sample_state in zip(self.samples, sample_states):
            if sample_state:
                sample.play()

    def play_sample(self, sample_number):
        self.samples[sample_number].play()
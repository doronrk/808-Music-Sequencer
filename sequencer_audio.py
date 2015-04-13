import wave
import sys
import pygame

class SequencerAudio(object):

    def __init__(self, sample_files):
        pygame.mixer.init()
        self.samples = [pygame.mixer.Sound(filename) for filename in sample_files]

    def play_samples(self, sample_states):
        for sample, sample_state in zip(self.samples, sample_states):
            if sample_state:
                sample.play()
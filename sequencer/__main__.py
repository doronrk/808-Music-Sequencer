import Tkinter
import sys
from os import listdir
from controller import Controller

if not len(sys.argv) == 2:
    print 'usage: python sequencer [relative_path_to_sample_folder]'
    sys.exit()
sample_folder_path = sys.argv[1]
try:
    files_in_sample_folder = listdir(sample_folder_path)
except OSError:
    print 'Could not locate sample folder'
    sys.exit()
wav_files_in_sample_folder = [sample_folder_path + '/' + sample for sample in files_in_sample_folder if sample[-4:] == '.wav']
if len(wav_files_in_sample_folder) == 0:
    print 'Could not locate any .wav files in the sample folder'
    sys.exit()

using_audio_out = True
try:
    from audio import Audio
    print 'Pygame audio supported, outputting samples to audio out'
except ImportError:
    using_audio_out = False
    #from sequencer_console_output import *
    print 'Pygame audio not supported, outputting sample names to console'
    print 'Please install Pygame for audio out'

root = Tkinter.Tk()
root.withdraw()
app = Controller(root, wav_files_in_sample_folder, using_audio_out)
root.title("Sequencer")
root.mainloop()
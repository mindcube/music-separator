import os
from pathlib import Path
import torchaudio
# Although torchaudio.set_audio_backend is deprecated, we still include it if needed:
torchaudio.set_audio_backend("sox_io")
import soundfile as sf

# Monkey-patch torchaudio.save to use soundfile for writing wav files
_original_save = torchaudio.save
def patched_save(filepath, src, sample_rate, *, format=None, **kwargs):
    # If format is not provided or is wav, use soundfile to write the file.
    if format is None or str(format).lower() == "wav":
        # Ensure the tensor is on CPU and convert to numpy.
        tensor_data = src.cpu().numpy()
        # torchaudio tensors are typically (channels, samples); soundfile expects (samples, channels)
        if tensor_data.ndim == 2:
            tensor_data = tensor_data.T
        # Write using sf.write; you may adjust the subtype (PCM_16) if needed.
        sf.write(filepath, tensor_data, sample_rate, format="WAV", subtype="PCM_16")
        return
    else:
        return _original_save(filepath, src, sample_rate, format=format, **kwargs)
torchaudio.save = patched_save

from demucs.separate import main as demucs_separate_main
from tqdm import tqdm

class MusicSeparator:
    def __init__(self, output_dir="separated_tracks"):
        # No instance needed when using the CLI function
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def process_song(self, input_file):
        # Create output directory for this specific song
        song_name = Path(input_file).stem
        song_dir = self.output_dir / song_name
        song_dir.mkdir(exist_ok=True)

        print(f"Processing {song_name}...")

        # Configure the arguments for the Demucs CLI separation
        args = [
            "-n", "htdemucs",    # choose the model; change this to "mdx_extra" if preferred
            "-d", "cpu",         # device to run on; change to "cuda" if available
            "-o", str(song_dir), # output directory
            input_file,          # input audio file
        ]
        demucs_separate_main(args)
        print(f"Finished processing {song_name}")

def main():
    # Initialize the separator
    separator = MusicSeparator()

    # Process a single file
    input_file = "input.wav"  # Replace with your input file
    separator.process_song(input_file)

if __name__ == "__main__":
    main()
import os
import librosa

import numpy as np
import soundfile as sf

PATH = "/home/pgoliszewski/Desktop/dataset-voice"
OUTPUT_PATH = "/home/tskrzypczak/Desktop/dataset_voice"


def split_by_tsec_time(file_path, time):
    sr_file = librosa.core.get_samplerate(au_path)

    loaded_audio, _ = librosa.core.load(au_path, sr_file)
    no_samples = loaded_audio.shape[0] // (sr_file * time)
    leftovers = (loaded_audio.shape[0] % (sr_file * time))

    if leftovers > (sr_file * time / 2):
        to_pad = sr_file * time - (loaded_audio.shape[0] % (sr_file * time))
        loaded_audio = np.concatenate((loaded_audio, np.zeros(to_pad)))
    else:
        loaded_audio = loaded_audio[:-leftovers]

    samples = np.array_split(loaded_audio, no_samples)
    return sr_file, samples

def save_samples(audio_sample, sr, orig_fname, dest_path, no_sample):
    ext = ".ogg"
    orig_fname, _ = orig_fname.split(".")

    out_fpath = os.path.join(dest_path, orig_fname + str(no_sample) + ext)
    sf.write(out_fpath, audio_sample, sr)

# sampling_rate = {}

for lang_fold in os.listdir(PATH):
    lang_path = os.path.join(PATH, lang_fold)
    output_lang_path = os.path.join(OUTPUT_PATH, lang_fold)

    os.makedirs(output_lang_path, exist_ok=True)  # succeeds even if directory exists.

    for au_fname in os.listdir(lang_path):
        au_path = os.path.join(lang_path, au_fname)
        sr, samples = split_by_tsec_time(lang_path, 5)

        for idx, s in enumerate(samples):
            save_samples(s, sr, au_fname, output_lang_path, idx)

# scripts/preprocess.py

import os
import yaml
import mne
from mne_bids import BIDSPath, read_raw_bids
from pathlib import Path
import numpy as np
import argparse
from scripts.seed_everything import set_global_seed  # Buat modul seed

def load_config(path="config/preprocessing.yaml"):
    with open(path, "r") as file:
        return yaml.safe_load(file)

def preprocess_subject(subject_id, config, raw_dir, processed_dir):
    print(f"🔄 Processing subject: {subject_id}")

    bids_path = BIDSPath(subject=subject_id, task=config['task'], root=raw_dir, extension=".edf")
    raw = read_raw_bids(bids_path=bids_path, verbose=False)

    # 1. Bandpass Filter
    raw.filter(l_freq=config['filter']['l_freq'], h_freq=config['filter']['h_freq'])

    # 2. Set montage (jika diperlukan)
    if config['montage']:
        raw.set_montage(config['montage'])

    # 3. ICA
    ica = mne.preprocessing.ICA(n_components=config['ica']['n_components'], random_state=config['seed'])
    ica.fit(raw)
    raw = ica.apply(raw)

    # 4. Epoching
    events, event_id = mne.events_from_annotations(raw)
    epochs = mne.Epochs(raw, events, event_id=event_id,
                        tmin=config['epoch']['tmin'],
                        tmax=config['epoch']['tmax'],
                        baseline=config['epoch']['baseline'],
                        preload=True)

    # 5. Normalisasi
    data = epochs.get_data()  # shape: (n_epochs, n_channels, n_times)
    data = (data - np.mean(data, axis=-1, keepdims=True)) / np.std(data, axis=-1, keepdims=True)

    # 6. Simpan hasil
    save_path = processed_dir / f"sub-{subject_id}_epo.npy"
    np.save(save_path, data)
    print(f"✅ Saved preprocessed data to {save_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='config/preprocessing.yaml')
    args = parser.parse_args()

    config = load_config(args.config)
    set_global_seed(config['seed'])

    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    subjects = config['subjects']
    for subject_id in subjects:
        preprocess_subject(subject_id, config, raw_dir, processed_dir)

if __name__ == "__main__":
    main()


import yaml
from models.eeg_cnn import EEGCNN
from models.eeg_transformer import EEGTransformer
from scripts.seed_everything import set_global_seed

def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)

def main():
    config = load_config("config/training.yaml")
    set_global_seed(config['seed'])

    model_type = config['model_type']
    if model_type == "cnn":
        model = EEGCNN()
    else:
        model = EEGTransformer()

    print(f"🧠 Model Loaded: {model_type.upper()}")

if __name__ == "__main__":
    main()


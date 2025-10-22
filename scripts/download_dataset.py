import os

def download_openneuro_dataset(dataset_id="ds003521", destination="data/raw"):
    os.system(f"npx openneuro download --dataset={dataset_id} --snapshot=1.0.1 --destination={destination}")

if __name__ == "__main__":
    download_openneuro_dataset()


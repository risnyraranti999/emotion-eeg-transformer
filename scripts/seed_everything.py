# scripts/seed_everything.py
import random
import numpy as np
import torch

def set_global_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    print(f"🌱 Global seed set to {seed}")


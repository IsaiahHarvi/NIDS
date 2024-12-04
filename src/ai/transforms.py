import numpy as np
import torch


class MinMaxTransform(torch.nn.Module):
    def __init__(self, min_val=0.0, max_val=1.0):
        self.min_val = min_val
        self.max_val = max_val

    def __call__(self, x: np.ndarray) -> torch.Tensor:
        x_min = x.min(axis=0, keepdims=True)[0]
        x_max = x.max(axis=0, keepdims=True)[0]
        scaled_x = (x - x_min) / (x_max - x_min) * (
            self.max_val - self.min_val
        ) + self.min_val
        return scaled_x

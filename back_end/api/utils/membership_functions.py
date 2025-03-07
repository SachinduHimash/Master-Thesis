import numpy as np


def sigmoid(x, k, c):
    return 1 / (1 + np.exp(-k * (x - c)))

def bell_shaped(x, b, c):
    return np.exp(-((x - b) ** 2) / (2 * c ** 2))

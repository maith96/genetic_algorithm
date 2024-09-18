import math
from .crossover import cross_genomes
import numpy as np

def softmax(scores):
    """
    Compute the softmax of a list of scores.

    Args:
        scores (list of float): List of scores.

    Returns:
        list of float: Softmax probabilities.
    """
    # Normalize scores by subtracting the maximum score to prevent large exponentials
    probabilities = scores / np.sum(scores)
    return probabilities
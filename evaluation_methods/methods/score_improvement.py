import numpy as np


# Sample alignment scores (pre- and post-fuzzy modification)
# pre_fuzzy_scores = np.array([5.2, 6.1, 4.7, 6.8, 7.0])
# post_fuzzy_scores = np.array([7.8, 8.5, 6.9, 8.3, 8.8])

def score_improvement(pre_fuzzy_scores, post_fuzzy_scores):
  


    # Compute mean score improvement
    score_improvement = np.mean(post_fuzzy_scores - pre_fuzzy_scores)
    return score_improvement
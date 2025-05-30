import numpy as np


# Sample alignment scores (pre- and post-fuzzy modification)
pre_fuzzy_scores = np.array([7.5,6.5,7.0,8,7.5,8,7.5,7,7.5,8,7.5,8,7.5,7,7.5,8,7.5,8,8,7.5,8,8,7.5,8,8,7.5,8,8.5,7.5,8,9,8.5,9,7,6.5,7,8.5,7.5,8,8,7.5,8,7,6.5,7,8,7.5,8,7,6.5,7,6.5,5.5,6,6,5,5.5,6,4.5,6,6.5,5.5,6,6.5,5.5,6.5,7.5,7,7.5,6.5,6,7])
post_fuzzy_scores = np.array([9,9.5,9,7,8.5,7,8,8.5,8,6.5,7,6.5,6.5,6.5,6,7.5,8.5,7.5,7.5,8.5,7.5,7.5,8,7.5,7.5,9,7.5,7,8.5,7,7,9.5,7,9,9.5,9,9.5,9.5,9,9.5,9.5,9.5,7,6.5,7,9.5,9,9,9,8.5,8.5,9,9.5,9,9.5,9,9.5,9,9,8.5,8.5,9,8,9,9,9,9.5,9,9,9,8.5,8])

# pre_fuzzy_scores = np.array([7.5,6.5,7.0])
# post_fuzzy_scores = np.array([9,9.5,9])

def score_improvement(pre_fuzzy_scores, post_fuzzy_scores):
  


    # Compute mean score improvement
    score_improvement = np.mean(post_fuzzy_scores - pre_fuzzy_scores)
    return score_improvement

print("Score Improvement: ", score_improvement(pre_fuzzy_scores, post_fuzzy_scores))
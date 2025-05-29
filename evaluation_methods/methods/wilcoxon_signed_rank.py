from scipy.stats import wilcoxon
import numpy as np


pre_fuzzy_scores = np.array([7.5,6.5,7.0,8,7.5,8,7.5,7,7.5,8,7.5,8,7.5,7,7.5,8,7.5,8,8,7.5,8,8,7.5,8,8,7.5,8,8.5,7.5,8,9,8.5,9,7,6.5,7,8.5,7.5,8,8,7.5,8,7,6.5,7,8,7.5,8,7,6.5,7,6.5,5.5,6,6,5,5.5,6,4.5,6,6.5,5.5,6,6.5,5.5,6.5,7.5,7,7.5,6.5,6,7])
post_fuzzy_scores = np.array([9,9.5,9,7,8.5,7,8,8.5,8,6.5,7,6.5,6.5,6.5,6,7.5,8.5,7.5,7.5,8.5,7.5,7.5,8,7.5,7.5,9,7.5,7,8.5,7,7,9.5,7,9,9.5,9,9.5,9.5,9,9.5,9.5,9.5,7,6.5,7,9.5,9,9,9,8.5,8.5,9,9.5,9,9.5,9,9.5,9,9,8.5,8.5,9,8,9,9,9,9.5,9,9,9,8.5,8])


# pre_fuzzy_scores = np.array([7.5,6.5,7.0])
# post_fuzzy_scores = np.array([9,9.5,9])


def wilcoxon_signed_rank(pre_fuzzy_scores, post_fuzzy_scores):
    # Compute Wilcoxon Signed-Rank Test
    stat, p_value = wilcoxon(pre_fuzzy_scores, post_fuzzy_scores)
    print("Wilcoxon Test Statistic:", stat, "p-value:", p_value)

    # Interpret significance
    if p_value < 0.05:
        print("Statistically significant improvement (p < 0.05)")
    else:
        print("No significant improvement (p >= 0.05)")
        
wilcoxon_signed_rank(pre_fuzzy_scores, post_fuzzy_scores)

from scipy.stats import wilcoxon


# pre_fuzzy_scores = np.array([5.2, 6.1, 4.7, 6.8, 7.0])
# post_fuzzy_scores = np.array([7.8, 8.5, 6.9, 8.3, 8.8])

def wilcoxon_signed_rank(pre_fuzzy_scores, post_fuzzy_scores):
    # Compute Wilcoxon Signed-Rank Test
    stat, p_value = wilcoxon(pre_fuzzy_scores, post_fuzzy_scores)
    print("Wilcoxon Test Statistic:", stat, "p-value:", p_value)

    # Interpret significance
    if p_value < 0.05:
        print("Statistically significant improvement (p < 0.05)")
    else:
        print("No significant improvement (p >= 0.05)")

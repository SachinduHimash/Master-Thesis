from scipy.stats import wilcoxon

# Compute Wilcoxon Signed-Rank Test
stat, p_value = wilcoxon(pre_fuzzy_scores, post_fuzzy_scores)
print("Wilcoxon Test Statistic:", stat, "p-value:", p_value)

# Interpret significance
if p_value < 0.05:
    print("Statistically significant improvement (p < 0.05)")
else:
    print("No significant improvement (p >= 0.05)")
from collections import Counter
from scipy.spatial.distance import jensenshannon
import numpy as np

def compute_token_distribution(text, vocab):
    tokens = text.split()
    token_counts = Counter(tokens)
    total_tokens = len(tokens)
    
    # Normalize frequencies and match vocabulary
    return np.array([token_counts.get(word, 0) / total_tokens for word in vocab])

# Example responses
pre_fuzzy_text = "Humanitarian aid is crucial in times of crisis."
post_fuzzy_text = "Providing humanitarian assistance is essential during emergencies."

# Create a shared vocabulary
vocab = set(pre_fuzzy_text.split()).union(set(post_fuzzy_text.split()))

# Compute token probability distributions
pre_dist = compute_token_distribution(pre_fuzzy_text, vocab)
post_dist = compute_token_distribution(post_fuzzy_text, vocab)

# Compute JSD
jsd_value = jensenshannon(pre_dist, post_dist)
print("Jensen-Shannon Divergence:", jsd_value)
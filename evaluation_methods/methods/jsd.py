from collections import Counter
from scipy.spatial.distance import jensenshannon
import numpy as np

def compute_token_distribution(text, vocab):
    tokens = str(text).split()
    token_counts = Counter(tokens)
    total_tokens = len(tokens)
    
    # Normalize frequencies and match vocabulary
    return np.array([token_counts.get(word, 0) / total_tokens for word in vocab])



def jensen_shannon(pre_fuzzy_text , post_fuzzy_text):


    # Create a shared vocabulary
    vocab = set(str(pre_fuzzy_text).split()).union(set(str(post_fuzzy_text).split()))
    
    # Compute token probability distributions
    pre_dist = compute_token_distribution(pre_fuzzy_text, vocab)
    post_dist = compute_token_distribution(post_fuzzy_text, vocab)
    


    # Compute JSD
    jsd_value = jensenshannon(pre_dist, post_dist)
    return jsd_value
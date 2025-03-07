from collections import Counter
from scipy.stats import entropy

def compute_entropy(text):
    tokens = text.split()  # Simple whitespace tokenization
    token_counts = Counter(tokens)
    total_tokens = len(tokens)

    # Probability distribution of tokens
    token_probs = [count / total_tokens for count in token_counts.values()]

    # Compute Shannon Entropy
    return entropy(token_probs, base=2)

# Example responses
pre_fuzzy_text = "Humanitarian aid is crucial in times of crisis."
post_fuzzy_text = "Providing humanitarian assistance is essential during emergencies."

# Compute entropy values
pre_entropy = compute_entropy(pre_fuzzy_text)
post_entropy = compute_entropy(post_fuzzy_text)

print("Entropy Reduction:", pre_entropy - post_entropy)
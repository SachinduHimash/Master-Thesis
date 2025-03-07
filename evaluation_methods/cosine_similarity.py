from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Example responses
pre_fuzzy_text = "Humanitarian aid is crucial in times of crisis."
post_fuzzy_text = "Providing humanitarian assistance is essential during emergencies."

# Convert texts to TF-IDF vectors
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform([pre_fuzzy_text, post_fuzzy_text])

# Compute Cosine Similarity
cos_sim = cosine_similarity(vectors[0], vectors[1])
print("Cosine Similarity:", cos_sim[0][0])
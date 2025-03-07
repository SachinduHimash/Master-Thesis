from sklearn.metrics.pairwise import euclidean_distances
from sklearn.feature_extraction.text import TfidfVectorizer

# Example responses
pre_fuzzy_text = "Humanitarian aid is crucial in times of crisis."
post_fuzzy_text = "Providing humanitarian assistance is essential during emergencies."

# Convert texts to TF-IDF vectors
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform([pre_fuzzy_text, post_fuzzy_text])
# Compute Euclidean Distance
euclidean_dist = euclidean_distances(vectors[0], vectors[1])
print("Euclidean Distance:", euclidean_dist[0][0])

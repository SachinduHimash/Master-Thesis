from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def euclidean_distance(pre_fuzzy_text, post_fuzzy_text):

    # Convert texts to TF-IDF vectors
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([pre_fuzzy_text, post_fuzzy_text])
    # Compute Euclidean Distance
    euclidean_dist = euclidean_distances(vectors[0], vectors[1])
    cosine_similarity_value = cosine_similarity(vectors[0], vectors[1])

    return euclidean_dist[0][0], cosine_similarity_value[0][0]

from sklearn.metrics.pairwise import cosine_similarity

from sklearn.feature_extraction.text import TfidfVectorizer




def cosine_similarity(pre_fuzzy_text = "", post_fuzzy_text =""):
   
    # Convert texts to TF-IDF vectors
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([pre_fuzzy_text, post_fuzzy_text])

    # Compute Cosine Similarity
    cos_sim = cosine_similarity(vectors[0], vectors[1])
    return cos_sim[0][0]


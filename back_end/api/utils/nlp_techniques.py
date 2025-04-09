import requests
import spacy
from sentence_transformers import SentenceTransformer, util
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from gensim import corpora
from sentence_transformers import CrossEncoder
import asyncio
import aiohttp
from functools import lru_cache
from nltk.corpus import wordnet

nlp = spacy.load("en_core_web_sm")

def evaluate_semantic_similiarity(text,keyword):

    # Example using spaCy
    nlp = spacy.load('en_core_web_md')
    paragraph = text
    word = keyword
    doc = nlp(paragraph)
    token = nlp(word)

    similarity = doc.similarity(token)

    # Example using Sentence Transformers
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Load a small Sentence Transformer model
    paragraph_embedding = model.encode(paragraph, convert_to_tensor=True)
    word_embedding = model.encode(word, convert_to_tensor=True)
    cosine_similarity = util.cos_sim(paragraph_embedding, word_embedding)

    
    return round(((similarity*100 + cosine_similarity.item()*100)/2), 2)
    
# def evaluate_entity_recognition(text,entities):
    
#     entities = [entity.lower() for entity in entities]  # Normalize list
    
#     doc = nlp(text)
#     total_words = len([token.text for token in doc if token.is_alpha])
#     matching_words = set()

#     # Debug detected entities
#     for ent in doc.ents:
#         entity_text = ent.text.lower().strip()
#         if entity_text in entities:
#             matching_words.add(entity_text)
#         else:
#             # Query ConceptNet
#             response = requests.get(f"https://api.conceptnet.io/c/en/{entity_text}")
#             if response.status_code == 200:
#                 edges = response.json().get("edges", [])
#                 related_concepts = [edge.get("start", {}).get("label", "").lower() for edge in edges]
#                 if any(entity in related_concepts for entity in entities):
#                     matching_words.add(entity_text)

#     # Token-based fallback matching
#     for token in doc:
#         token_text = token.text.lower().strip()
#         if token_text in entities:
#             matching_words.add(token_text)
            

#     percentage_score = (len(matching_words) /
#                         total_words) * 100 if total_words > 0 else 0
#     return round(percentage_score, 2)



def get_synonyms(word):
    """Retrieve synonyms using WordNet to avoid API calls."""
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().lower().replace("_", " "))
    return synonyms

def evaluate_entity_recognition(text, entities):
    entities = set(entity.lower() for entity in entities)  # Normalize entities
    expanded_entities = entities.copy()

    # Expand entities with synonyms
    for entity in entities:
        expanded_entities.update(get_synonyms(entity))

    doc = nlp(text)
    total_words = sum(1 for token in doc if token.is_alpha)
    matching_words = {token.text.lower() for token in doc if token.text.lower() in expanded_entities}

    # Calculate score
    percentage_score = (len(matching_words) / total_words) * 100 if total_words > 0 else 0
    return round(percentage_score, 2)

def evaluate_sentiment_alignment(text,keyword):

    analyzer = SentimentIntensityAnalyzer()
    paragraph_sentiment = analyzer.polarity_scores(text)
    word_sentiment = analyzer.polarity_scores(keyword)

    similarity = 1 - abs(paragraph_sentiment['compound'] - word_sentiment['compound'])
    return max(0, min(100, similarity * 100))

def evaluate_cross_encoder_scoring(text,keyword):
    cross_encoder = CrossEncoder('cross-encoder/stsb-roberta-base')
    score = cross_encoder.predict([(text, keyword)])
    return score[0] * 100
    

from .nlp_techniques import evaluate_cross_encoder_scoring,evaluate_entity_recognition,evaluate_semantic_similiarity,evaluate_sentiment_alignment


def evaluate_text(text,keyword,entities):
        
    sentiment_score = evaluate_sentiment_alignment(text, keyword)
    cross_encoder_score = evaluate_cross_encoder_scoring(text, keyword)
    semantic_similarity_score = evaluate_semantic_similiarity(text, keyword)
    # entity_recognition_score = evaluate_entity_recognition(text, entities)
    scores = [
        sentiment_score,
        cross_encoder_score,
        semantic_similarity_score,
        # entity_recognition_score
    ]
    
    # Calculate the average score
    average_score = sum(scores) / len(scores)
    return average_score
    
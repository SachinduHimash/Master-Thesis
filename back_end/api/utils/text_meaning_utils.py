from transformers import pipeline

classifier = pipeline("zero-shot-classification")

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def getTheMeaningofText(text):

    candidate_labels = ["Humanity","Focus on Life and Well-being", "Targeting Vulnerable Populations", "Comprehensive Care","Preserving Dignity"]

    # Generate the summary
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
    

    categories1 = classifier(text, candidate_labels)['labels']
    values1 = classifier(text, candidate_labels)['scores']
    
    categories2 = classifier(summary[0]['summary_text'], candidate_labels)['labels']
    values2 = classifier(summary[0]['summary_text'], candidate_labels)['scores']
    
    
    averaged_data = {}

    for category, value in zip(categories1, values1):
        averaged_data[category] = value

    # Iterate through the second array to calculate the average
    for category, value in zip(categories2, values2):
        if category in averaged_data:
            averaged_data[category] = (averaged_data[category] + value) / 2

    return averaged_data
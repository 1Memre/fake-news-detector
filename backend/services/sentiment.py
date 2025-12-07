from textblob import TextBlob

def analyze_sentiment(text: str):
    """
    Analyzes sentiment using TextBlob.
    Returns polarity (-1 to 1), subjectivity (0 to 1), and a label.
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    if polarity > 0.1:
        label = "Positive"
    elif polarity < -0.1:
        label = "Negative"
    else:
        label = "Neutral"
        
    return polarity, subjectivity, label

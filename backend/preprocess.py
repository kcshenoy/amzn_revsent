import re
from transformers import pipeline

def clean_text(review):

    combined = review['review_title'] + '. ' + review['review_comment']

    combined = re.sub(r'<.*?>', '', combined)  # Remove HTML tags
    combined = re.sub(r'http\S+', '', combined)  # Remove URLs

    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "\U0001F1E0-\U0001F1FF"  # Flags
        "\U00002702-\U000027B0"  # Miscellaneous Symbols
        "\U000024C2-\U0001F251"  # Enclosed Characters
        "]+",
        flags=re.UNICODE
    )
    combined = emoji_pattern.sub(r'', combined)

    combined = combined.strip()

    return combined

def product_sentiment_score(reviews):
    review_text = [clean_text(review) for review in reviews]
    sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
    model_sentiment = [sentiment_analyzer(review) for review in review_text]
    return model_sentiment



from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv 

from flask import Flask
from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect
from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import scrape_reviews, get_review_percentages
from get_asin import get_asin
from preprocess import product_sentiment_score
import os

load_dotenv('.env')

app = Flask(__name__)

# Load config from config.py
app.config.from_object('config.Config')
# print(app.config)

# Initialize PyMongo to work with MongoDB
# mongo = PyMongo(app)

CORS(app)  # Allow cross-origin requests from React

@app.route('/analyze', methods=['GET','POST'])
def analyze():
    print('running')
    data = request.json
    url = data.get('url')
    response = {}

    asin = get_asin(url)
    stars = get_review_percentages(url)

    reviews = scrape_reviews(asin)

    review_scores = product_sentiment_score(reviews)

    response['stars'] = stars
    response['reviews'] = reviews
    response['scores'] = review_scores[0]
    response['product_sentiment'] = sum(review_scores[0])/review_scores[1]

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
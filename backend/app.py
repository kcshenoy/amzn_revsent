from flask import Flask
from flask_pymongo import PyMongo
from auth import auth  # Blueprint for authentication
from dotenv import load_dotenv 

from flask import Flask
from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect
from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import scrape_reviews, get_review_percentages
from get_asin import get_asin
import os

load_dotenv('.env')

app = Flask(__name__)

# Load config from config.py
app.config.from_object('config.Config')
# print(app.config)

# Initialize PyMongo to work with MongoDB
mongo = PyMongo(app)

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

    response['stars'] = stars
    response['reviews'] = reviews


    # # Scrape and analyze
    # reviews = fetch_reviews(url)
    # sentiment = analyze_sentiment(reviews)

    # # Prepare chart data (dummy for now)
    # chart_data = {"1 Star": 10, "2 Star": 15, "3 Star": 25, "4 Star": 30, "5 Star": 20}

    # return jsonify({
    #     "sentiment": sentiment,
    #     "chartData": chart_data
    # })

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask
from flask_pymongo import PyMongo
from auth import auth  # Blueprint for authentication

from flask import Flask
from flask_pymongo import PyMongo
from auth import auth  # Blueprint for authentication
from flask_wtf.csrf import CSRFProtect
from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import scrape_reviews
from get_asin import get_asin
import os

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
    print(data)
    url = data.get('url')
    print(url)

    asin = get_asin(url)

    scraped = scrape_reviews(asin)

    # # Scrape and analyze
    # reviews = fetch_reviews(url)
    # sentiment = analyze_sentiment(reviews)

    # # Prepare chart data (dummy for now)
    # chart_data = {"1 Star": 10, "2 Star": 15, "3 Star": 25, "4 Star": 30, "5 Star": 20}

    # return jsonify({
    #     "sentiment": sentiment,
    #     "chartData": chart_data
    # })

    return jsonify(scraped)


if __name__ == '__main__':
    app.run(debug=True)
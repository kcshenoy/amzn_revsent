import os
from dotenv import load_dotenv

class Config:
    # MongoDB URI for connecting to your database
    MONGO_URI = "mongodb+srv://kri665664:amzn_reviews@amzn-reviews.yscx1.mongodb.net/?retryWrites=true&w=majority&appName=amzn-reviews" # Default to localhost if not set
    JWT_SECRET_KEY = "amznrevapp-1124" # Use environment variable for security
    SECRET_KEY = "amznrevappsecret-1124"  # Flask app secret key for sessions
    AMZN_API_URL = "https://real-time-amazon-data.p.rapidapi.com/product-reviews" # Amazon API url
    AMZN_API_KEY = "2a61fad4b0msh025dc894ebfee18p11d95ajsn50d49359dcf8" # Amazon API key 


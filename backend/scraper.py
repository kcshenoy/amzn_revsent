from flask import current_app
import requests

def scrape_reviews(asin):
    page_count = 3
    q_strings = []
    responses = []

    for i in range(1, page_count):
        querystring = {"asin":asin,"country":"US","sort_by":"TOP_REVIEWS","star_rating":"ALL","verified_purchases_only":"false","images_or_videos_only":"false","current_format_only":"false","page":f"{i}"}
        q_strings.append(querystring)

    headers = {
	"x-rapidapi-key": current_app.config.get("AMZN_API_KEY"),
	"x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
    }

    for q in q_strings:
        resp = requests.get(current_app.config.get("AMZN_API_URL"), headers=headers, params=q)
        responses.append(resp.json()['data']['reviews'])

    return(responses)
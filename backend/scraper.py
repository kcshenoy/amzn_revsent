from flask import current_app
from playwright.sync_api import sync_playwright
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

def get_review_percentages(url):
    with sync_playwright() as p:
        # Launch the browser in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to the Amazon product page
        page.goto(url, timeout=60000)  # Timeout increased to handle delays

        # Extract the histogram table (review percentages section)
        try:
            # Wait for the review histogram table to load
            page.wait_for_selector("#histogramTable", timeout=10000)

            # Locate all review rows in the histogram table
            star_rows = page.query_selector_all("#histogramTable li")

            # Extract star ratings and percentages
            i = 0
            star_percentages = {}
            for star_row in star_rows:
                # Extract the star label (e.g., "5 star")
                star_label = star_row.text_content().split('star')[i]
                i += 1

                # Extract the percentage (e.g., "85%")
                percentage = star_row.query_selector("span").inner_text().splitlines()[1]
                star_percentages[f"{star_label} star"] = percentage

            return star_percentages

        except Exception as e:
            print(f"Error scraping the page: {e}")
            return None

        finally:
            browser.close()
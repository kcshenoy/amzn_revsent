from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from playwright.sync_api import sync_playwright

import requests
import re
from bs4 import BeautifulSoup
import urllib.robotparser

url = 'https://www.amazon.ca/'

# Function to get and parse robots.txt
def get_robots_txt():
    robots_url = url + "/robots.txt"
    response = requests.get(robots_url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Function to parse robots.txt and check if scraping is allowed
def is_allowed_to_scrape(url, user_agent='*'):
    rp = urllib.robotparser.RobotFileParser()
    robots_url = url + '/robots.txt'
    rp.set_url(robots_url)
    rp.read()
    return rp.can_fetch(user_agent, url)

# Function to extract ASIN from the URL using regex
def extract_asin_from_url(url):
    asin_match = re.search(r'/dp/([A-Za-z0-9]{10})', url)
    if asin_match:
        return asin_match.group(1)  # Return the ASIN
    else:
        return None  # ASIN not found in the URL

# Function to scrape ASIN from the HTML of the page (if URL doesn't contain it)
def scrape_asin_from_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Look for the ASIN
    asin = soup.find('input', {'id': 'ASIN'}) 
    if asin:
        return asin.get('value')  # Return the ASIN
    else:
        return None  # ASIN not found in the HTML


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




# Main function to scrape ASIN
def get_asin(url):
    # Check if scraping the URL is allowed according to robots.txt
    if not is_allowed_to_scrape(url):
        print("Scraping is disallowed for this URL based on robots.txt.")
        return None

    # Extract the ASIN from the URL
    asin = extract_asin_from_url(url)
    if not asin:
        print("ASIN not found in the URL, scraping HTML for ASIN...")
        asin = scrape_asin_from_html(url)
    
    return asin


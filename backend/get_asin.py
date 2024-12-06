import requests
import re
from bs4 import BeautifulSoup
import urllib.robotparser

url = 'https://www.amazon.ca/'


'''
is_allowed_to_scrape takes a url, grabs the robots file and checks where url is scrapable
'''
def is_allowed_to_scrape(url, user_agent='*'):
    rp = urllib.robotparser.RobotFileParser()
    robots_url = url + '/robots.txt'
    rp.set_url(robots_url)
    rp.read()
    return rp.can_fetch(user_agent, url)

'''
extract_asin_from_url takes a url and checks if it can get the amazon ASIN from the link itself
'''
def extract_asin_from_url(url):
    asin_match = re.search(r'/dp/([A-Za-z0-9]{10})', url)
    if asin_match:
        return asin_match.group(1)  # Return the ASIN
    else:
        return None  # ASIN not found in the URL

'''
scrape_asin_from_html scrapes the amazon ASIN from the website itself, returns it
'''
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


'''
get_asin returns the ASIN given an URL
'''
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


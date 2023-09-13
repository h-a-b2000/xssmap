import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def fetch_and_parse(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
    return None

def crawl(url):
    visited_urls = set()
    urls_to_crawl = [url]
    while urls_to_crawl:
        url = urls_to_crawl.pop(0)  # Get the next URL to crawl
        visited_urls.add(url)  # Add it to the visited URLs set

        # Fetch and parse the webpage
        soup = fetch_and_parse(url)
        if soup is not None:
            print(f"Crawling: {url}")

            # Extract links from the webpage
            for link in soup.find_all('a', href=True):
                link_url = link.get('href')
                if link_url:
                    # Make sure the URL is absolute
                    absolute_url = urljoin(url, link_url)

                    # Check if the absolute URL has not been visited or added to the queue
                    if absolute_url not in visited_urls and absolute_url not in urls_to_crawl:
                        urls_to_crawl.append(absolute_url)

    

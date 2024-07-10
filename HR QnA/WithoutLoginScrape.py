import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import os

visited_urls = set()
base_url = "https://www.cms.co.in/"
# start_url = "https://www.cms.co.in/aboutus-22_overview-3"
output_file = "_CMS_SCRAPED_.txt"

# Function to check if a URL is allowed to be crawled based on robots.txt


def is_allowed(url):
    parsed_url = urlparse(url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    try:
        response = requests.get(robots_url)
        if response.status_code == 200:
            lines = response.text.splitlines()
            for line in lines:
                if line.startswith("Disallow"):
                    if urljoin(base_url, line.split(":")[1].strip()) in url:
                        return False
        return True
    except requests.exceptions.RequestException:
        return False


def crawl(url):
    # Check if we've already visited this URL
    if url in visited_urls:
        return
    visited_urls.add(url)

    # Check if crawling is allowed by robots.txt
    if not is_allowed(url):
        print(f"Crawling disallowed by robots.txt: {url}")
        return

    # Send a GET request to the website
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return

    # Check if the content type is HTML
    if 'text/html' not in response.headers.get('Content-Type', ''):
        print(f"Skipping non-HTML content at {url}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract text from the parsed HTML
    text_content = soup.get_text()

    # Append the text content to the file
    with open(output_file, "a", encoding="utf-8") as file:
        file.write(f"URL: {url}\n{text_content}\n\n")

    print(f"Content from {url} appended to {output_file}")

    # Find all hyperlinks on the page
    for link in soup.find_all('a', href=True):
        # Resolve relative URLs
        next_url = urljoin(base_url, link['href'])

        # Follow only URLs within the same domain
        if next_url.startswith(base_url):
            crawl(next_url)
        # Sleep to avoid overwhelming the server
        time.sleep(1)


# Remove the output file if it already exists
if os.path.exists(output_file):
    os.remove(output_file)

# Start crawling from the start URL
crawl(base_url)

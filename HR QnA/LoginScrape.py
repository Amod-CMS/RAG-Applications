import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import os
import urllib3

# Suppress only the single InsecureRequestWarning from urllib3 needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


visited_urls = set()
base_url = "https://cdl.cms.co.in/group/cms"
start_url = "https://cdl.cms.co.in/group/cms"
login_url = "https://cdl.cms.co.in/web/cms/home?p_p_id=com_liferay_login_web_portlet_LoginPortlet&p_p_lifecycle=1&p_p_state=maximized&p_p_mode=view&refererPlid=33886&_com_liferay_login_web_portlet_LoginPortlet_javax.portlet.action=%2Flogin%2Flogin&_com_liferay_login_web_portlet_LoginPortlet_mvcRenderCommandName=%2Flogin%2Flogin"  # Replace with the actual login URL
# Replace with your username
_com_liferay_login_web_portlet_LoginPortlet_login = "----------------"
# Replace with your password
_com_liferay_login_web_portlet_LoginPortlet_password = "**********"
output_file = "cdl.txt"

session = requests.Session()

# Function to log in to the website

def login():
    # Replace these field names with the actual names used in the login form
    login_data = {
        # Replace with the actual username field name
        '_com_liferay_login_web_portlet_LoginPortlet_login': _com_liferay_login_web_portlet_LoginPortlet_login,
        # Replace with the actual password field name
        '_com_liferay_login_web_portlet_LoginPortlet_password': _com_liferay_login_web_portlet_LoginPortlet_password
    }

    response = session.post(login_url, data=login_data, verify=False)
    if response.status_code == 200:
        print("Login successful")
    else:
        print("Login failed")
        exit()


def crawl(url):
    # Check if we've already visited this URL
    if url in visited_urls:
        return
    visited_urls.add(url)

    # Send a GET request to the website
    try:
        response = session.get(url, verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return

    # Check if the content type is HTML
    if 'text/html' not in response.headers.get('Content-Type', ''):
        print(f"Skipping non-HTML content at {url}")
        return

    # Parse the HTML content
    try:
        soup = BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Failed to parse HTML content from {url}: {e}")
        return

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

# Log in to the website
login()

# Start crawling from the start URL
crawl(start_url)

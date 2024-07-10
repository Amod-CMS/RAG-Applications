from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import os

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

# Setup WebDriver
# Update with your path to chromedriver
service = ChromeService(executable_path='C:\\Users\\amod_nagpal.CMS\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)

visited_urls = set()
base_url = "https://cdl.cms.co.in/group/cms"
start_url = "https://cdl.cms.co.in/group/cms"
login_url = "https://cdl.cms.co.in/web/cms/home?p_p_id=com_liferay_login_web_portlet_LoginPortlet&p_p_lifecycle=1&p_p_state=maximized&p_p_mode=view&refererPlid=33886&_com_liferay_login_web_portlet_LoginPortlet_javax.portlet.action=%2Flogin%2Flogin&_com_liferay_login_web_portlet_LoginPortlet_mvcRenderCommandName=%2Flogin%2Flogin"  # Replace with the actual login URL
# Replace with your username
username = "amod_nagpal@cms.co.in"  # Replace with your username
password = "Suresh@101066"  # Replace with your password
output_file = "testing.txt"

# Function to log in to the website


def login():
    driver.get(login_url)

    # Replace with the actual element locators used in the login form
    username_field = wait.until(EC.presence_of_element_located(
        (By.ID, '_com_liferay_login_web_portlet_LoginPortlet_login')))  # Replace with the actual username field name
    password_field = wait.until(EC.presence_of_element_located(
        (By.ID, '_com_liferay_login_web_portlet_LoginPortlet_password')))  # Replace with the actual password field name

    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    # Wait for a unique element that indicates login success
    try:
        # Replace with an appropriate check for your site
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[text()='Logout']")))
        print("Login successful")
        return True
    except Exception as e:
        print("Login failed or timeout:", e)
        return False


def crawl(url):
    # Check if we've already visited this URL
    if url in visited_urls:
        return
    visited_urls.add(url)

    # Visit the URL
    driver.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(driver.page_source, 'html.parser')

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
if login():
    # Start crawling from the start URL
    crawl(start_url)
else:
    print("Unable to log in, stopping crawler.")

# Close the WebDriver
driver.quit()

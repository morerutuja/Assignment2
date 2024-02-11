#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import requests
from bs4 import BeautifulSoup
import csv


# In[2]:


# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
total=0
page_link = []

def scrape_links(driver):
    n=0
    global total
    global page_link
    links = driver.find_elements(By.CSS_SELECTOR, 'div.cfa-coveo a')
    for link in links:
        href = link.get_attribute('href')
        if href is not None:
            n=n+1
            page_link.append(href)
            print(href)
        
    total=total+n
    
def go_to_next_page(driver):
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "li.coveo-pager-next")
        # Using JavaScript
        driver.execute_script("arguments[0].click();", next_button)
        return True
    except NoSuchElementException:
        return False

url = 'https://www.cfainstitute.org/en/membership/professional-development/refresher-readings'
driver.get(url)

#scraping loop
while True:
    # Wait for content
    try:
        WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.cfa-coveo')))
        scrape_links(driver)
    except TimeoutException:
        print("Timed out waiting for page to load")
        break  
    if not go_to_next_page(driver):
        print("No more pages or next button not found.")
        break
    time.sleep(5)


# In[3]:


print(total)


# In[5]:


import requests
from bs4 import BeautifulSoup
import csv

urls = page_link.copy()

csv_file_path = 'extracted.csv'

# CSV headers
headers = ['Topic', 'Year', 'Level', 'Introduction Summary', 'Learning Outcomes', 'URL link', 'PDF link']


def safe_extract_text(soup, selector, attribute=None):
    element = soup.select_one(selector)
    if attribute:
        return element[attribute] if element and attribute in element.attrs else "None"
    return element.get_text(strip=True) if element else "None"

def extract_following_text(header):
    if header:
        content = []
        for sibling in header.find_next_siblings():
            if sibling.name == "h2":
                break  # Stop if we encounter another header
            content.append(sibling.get_text(strip=True))
        return " ".join(content)
    return "None"

with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()
    
    # Iterate over each URL in the list
    for url in urls:
        # Fetch the HTML content of the page
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the required information using safe_extract_text
        curriculum_year = safe_extract_text(soup, ".content-utility-curriculum")
        level = safe_extract_text(soup, ".content-utility-level")
        topic = safe_extract_text(soup, ".content-utility-topic")
        pdf_link = safe_extract_text(soup, "a.locked-content", "href")
        
        # Extract Introduction and Learning Outcomes
        introduction_header = soup.find("h2", text="Introduction")
        introduction_text = extract_following_text(introduction_header)
        
        learning_outcomes_header = soup.find("h2", text="Learning Outcomes")
        learning_outcomes_text = extract_following_text(learning_outcomes_header)
        
        # Write the extracted data to the CSV
        data = {
            "Topic": topic,
            "Year": curriculum_year,
            "Level": level,
            "Introduction Summary": introduction_text,
            "Learning Outcomes": learning_outcomes_text,
            "URL link": url,
            "PDF link": pdf_link
        }
        
        writer.writerow(data)


# In[ ]:





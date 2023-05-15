import csv
from typing import Tuple, Union

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from find_emails import find_emails


def browse_website() -> Union[str, None]:
    text = scrape_text_with_selenium(url)

    return text

    
def scrape_text_with_selenium() -> Tuple[WebDriver, str]:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    page_source = driver.execute_script("return document.body.outerHTML;")
    soup = BeautifulSoup(page_source, "html.parser")

    # Insert spaces between HTML elements
    for tag in soup():
        if tag.next_sibling:
            tag.insert_after(" ")
        if tag.previous_sibling:
            tag.insert_before(" ")

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = " ".join(chunk for chunk in chunks if chunk)

    return text

def close_browser(driver: WebDriver) -> None:
    driver.quit()



with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    with open('websites.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        # Initialize Chrome driver
        driver = webdriver.Chrome()
        print(driver)
        # Iterate over rows in CSV file
        for row in reader:
            # Get website URL from row
            if row:
                url = row[0]

                if url:

                    scraped_data = None

                    emails = list()

                    try:
                        driver.get("https://"+ url + "/contact")
                        # Scrape website and get scraped data as a string
                        scraped_data = browse_website("https://"+ url + "/contact")
                        emails = list(find_emails(scraped_data))

                    except Exception as e:
                        print("no contact page found")
                

                    if not emails:
                        try:
                            driver.get("https://"+ url + "/contact-us")
                            # Scrape website and get scraped data as a string
                            scraped_data = browse_website( "https://"+ url + "/contact-us")
                            emails = list(find_emails(scraped_data))

                        except Exception as e:
                            print("no contact-us page found")


                    if not emails:
                        try:
                            driver.get("https://"+ url)
                            # Scrape website and get scraped data as a string
                            scraped_data = browse_website( "https://"+ url)
                            emails = list(find_emails(scraped_data))

                        except Exception as e:
                            print("Error on home page")
            
                        
                    print(emails)

                    if emails:
                        writer.writerow([url, *emails])
                        
                else:
                    writer.writerow([""])
        close_browser(driver)
"""Selenium web scraping module."""
from __future__ import annotations
from typing import Tuple, Union

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def browse_website(url: str) -> Union[str, None]:
    text = scrape_text_with_selenium(url)

    return text

    
def scrape_text_with_selenium(url: str) -> Tuple[WebDriver, str]:
    driver = webdriver.Chrome()
    driver.get(url)

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
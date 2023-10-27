from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sys

def get_definition(query):
    url = "http://en.dict.naver.com/#/search?query=" + query.replace(" ", "+")

    # Utilize selenium and chromedriver to grab the target page source with options, quitting the driver afterwards
    val = Options()
    val.add_argument("--headless")
    val.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=val)
    driver.get(url)
    time.sleep(3)
    source = driver.page_source
    driver.quit()

    # Create a BeautifulSoup object with the source
    soup = BeautifulSoup(source, "lxml")

    # Return None if page signals query doesn't return a valid result
    if len(soup.find_all("div", class_="component_empty")) != 0:
        return

    # Try to grab definition(s), returning None on error
    try:
        # Grab current row
        row = soup.find_all("div", class_="row")[0]

        # Return None if section title doesn't match query
        if(row.find_all("div", class_="origin")[0].find_all("a")[0].find_all("strong")[0].text != query):
            return
        
        # Gather definitions
        definitions = [' '.join(x.text.strip().split()) for x in row.find_all("ul", class_="mean_list")[0].find_all("li", class_="mean_item")]

        # If successful return reply string with definitions list
        return "According to the Naver English-Korean Dictionary...\n\nDefinitions for " + query + "\n" + "\n".join(definitions) 
    except:
        return "Invalid word."

def main():
    user_input = input("Please enter a Korean word to translate or 'quit' to quit: ")
    while user_input != "quit":
        print(get_definition(user_input))

if __name__ == "__main__":
    main()

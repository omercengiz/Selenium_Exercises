import random
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import uuid


def initialize_browser():
    return webdriver.Chrome(ChromeDriverManager().install())


def search_and_scrape(browser, search_query, num_pages=5):
    entries_list = []
    date_list = []
    nickname_list = []

    browser.get("https://eksisozluk111.com/")
    browser.maximize_window()
    time.sleep(4)

    search_input = browser.find_element(By.XPATH, '//input[@id="search-textbox"]')
    search_input.send_keys(search_query)
    search_input.send_keys(Keys.ENTER)

    time.sleep(4)

    current_page_url = browser.current_url

    for _ in range(num_pages):
        random_page_number = random.randint(1, 1200)
        new_url = f"{current_page_url}?p={random_page_number}"
        browser.get(new_url)

        content_all = browser.find_elements(By.CSS_SELECTOR, 'div.content')
        date_all = browser.find_elements(By.CSS_SELECTOR, 'a.entry-date.permalink')
        nickname_all = browser.find_elements(By.CSS_SELECTOR, 'a.entry-author')

        date_list.extend(element.text for element in date_all)
        entries_list.extend(element.text for element in content_all)
        nickname_list.extend(element.text for element in nickname_all)

        time.sleep(3)

    return date_list, entries_list, nickname_list


def create_dataframe(date_list, entries_list, nickname_list):
    data = {
        'NewsID': [str(uuid.uuid4()) for _ in range(len(entries_list))],
        'Timestamp': date_list,
        'Nickname': nickname_list,
        'Entry': entries_list
    }

    return pd.DataFrame(data)


def main():
    browser = initialize_browser()

    try:
        search_query = 'Masterchef Türkiye'
        date_list, entries_list, nickname_list = search_and_scrape(browser, search_query)

        # Create the dataframe and save it to the Excel
        df = create_dataframe(date_list, entries_list, nickname_list)
        df.to_excel('entries_data.xlsx', index=False)

        # Set the display.max_colwidth option
        pd.set_option('display.max_colwidth', None)


    finally:
        browser.close()


if __name__ == "__main__":
    main()

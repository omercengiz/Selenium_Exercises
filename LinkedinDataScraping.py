# Importing necessary libraries
import os
import selenium
import json
import time
import pandas as pd
import itertools
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Read login credentials from config file
with open("config.json", "r") as config_file:
    config = json.load(config_file)

our_username = config.get("username", "")
our_password = config.get("password", "")

# LinkedIn login URL
url = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'

# Set up Chrome webdriver. We don't need to import any chromedriver.exe, regularly due to chrome versions
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url=url)


# Log into LinkedIn Page
def log_in(username, password):
    username = driver.find_element(by=By.XPATH, value="//input[@name ='session_key']")
    password = driver.find_element(by=By.XPATH, value="//input[@name ='session_password']")

    time.sleep(1)
    username.send_keys(our_username)
    time.sleep(1)
    password.send_keys(our_password)

    time.sleep(2)
    submit = driver.find_element(by=By.XPATH, value="//button[@type = 'submit']")
    submit.click()


# Search for people on LinkedIn
def search_people(search):
    search_button = driver.find_element(by=By.XPATH,
                                        value="//*[@id='global-nav-typeahead']/input")
    search_button.click()
    time.sleep(1)
    search_button.send_keys(search)
    time.sleep(2)
    search_button.send_keys(Keys.RETURN)
    time.sleep(6)

    buttons = driver.find_elements(by=By.TAG_NAME, value="button")
    time.sleep(2)
    people_button = [btn for btn in buttons if btn.text == 'Kişiler']
    people_button[0].click()


def select_country(country):
    time.sleep(3)
    country_button = driver.find_elements(by=By.XPATH,
                                          value="//li[@class ='search-reusables__primary-filter']")
    for i in country_button:
        if i.text == "Konumlar":
            i.click()
    time.sleep(1)

    placeholder = driver.find_element(by=By.XPATH, value="//input[@placeholder = 'Konum ekle']")
    placeholder.send_keys(country)
    time.sleep(1)
    placeholder.send_keys(Keys.DOWN)
    placeholder.send_keys(Keys.RETURN)

    time.sleep(4)


def navigate_to_next_page(page_number):
    current_url = driver.current_url
    p1, p2 = current_url.split("SEARCH&")
    next_url = p1 + "SEARCH&page=" + str(page_number)

    driver.get(next_url)
    time.sleep(3)


# Lists to store scraped data
name_list = []
role_list = []
url_list = []
company_list = []

# Scrape data from the current LinkedIn search page
def scrape_data():
    names = driver.find_elements(by=By.XPATH,
                                 value="//span[@dir='ltr']/span[1]")
    companies = driver.find_elements(by=By.XPATH,
                                     value="//p[starts-with(@class,'entity-result__summary')]")
    linkedin_urls = driver.find_elements(by=By.XPATH,
                                         value="//span[starts-with(@class, 'entity-result__title-text')]/a")
    linkedin_urls = [url.get_attribute("href") for url in linkedin_urls]
    roles = driver.find_elements(by=By.XPATH,
                                 value="//div[@class ='entity-result__primary-subtitle t-14 t-black t-normal']")

    lens = [len(names), len(companies), len(linkedin_urls), len(roles)]
    rang = min(lens)
    print(rang)
    for j in range(rang):
        if "search/" in linkedin_urls[j]:
            pass
        else:
            name_list.insert(j, names[j].text)
            role_list.insert(j, roles[j].text)
            company_list.insert(j, companies[j].text.split(' ')[2])
            url_list.insert(j, linkedin_urls[j])


title = "Machine Learning Engineer"
selected_country = "Almanya"
log_in(our_username, our_password)
time.sleep(10)

search_people(title)
select_country(selected_country)

for i in range(1, 2):
    navigate_to_next_page(i)
    scrape_data()

create_DB = str(input("To create database press: 'd',to continue press: 'c'"))

if create_DB == 'd':
    dic = {'Name': name_list, 'Role': role_list,
           'Company': company_list, 'LinkedIn': url_list,
           'Country': [selected_country for c in range(len(url_list))]}
    data = pd.DataFrame.from_dict(dic, orient='index').T.dropna()
    directory_path = 'C:\\Users\\alons\\PycharmProjects\\SeleniumWebScraping'
    file_path = f'{directory_path}\\ML_engineer_almanya.xlsx'

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    data.to_excel(file_path)

elif create_DB == 'c':
    pass

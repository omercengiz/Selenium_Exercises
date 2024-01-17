# import requirement packages and modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

browser = webdriver.Chrome(ChromeDriverManager().install())

url = "https://bulten.mserdark.com/"
browser.get(url)
browser.maximize_window()
time.sleep(2)

button = browser.find_element(By.XPATH, '//*[@id="entry"]/div[1]/div/div/div[1]/a/button')
button.click()

time.sleep(10)

content_all = browser.find_elements(By.XPATH, '//a[contains(@class, "pencraft pc-reset frontend-pencraft-Text-module__color-pub-secondary-text--OzRTa frontend-pencraft-Text-module__line-height-20--p0dP8 frontend-pencraft-Text-module__font-text--QmNJR frontend-pencraft-Text-module__size-14--Ume6q frontend-pencraft-Text-module__clamp--a1dYM frontend-pencraft-Text-module__clamp-1--qD_7y frontend-pencraft-Text-module__reset--dW0zZ")]')
time.sleep(5)

for element in content_all:
    print(element.text)

browser.close()
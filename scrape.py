import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By

import time

import pandas as pd

from selenium.webdriver.common.keys import Keys

def read_cas_data(csv_filepath="src/smiles_pine.csv"):
    df = pd.read_csv(csv_filepath)
    df = df[["cas", "name"]]
    return df 

def accept_cookies(driver,url):
    driver.get(url)
    time.sleep(3)
    cookies = driver.find_elements(By.ID, 'onetrust-accept-btn-handler')
    cookies[0].click()
    time.sleep(1)
    return



def get_vapour_pressures(cas,name, driver,url, byname=False):
    if byname:
        key = name
    else:
        key = cas
    driver.get(url)
    time.sleep(3)
    search = driver.find_elements(By.ID, "input-left-icon")
    search[0].send_keys(key)
    time.sleep(5)
    search[0].send_keys(Keys.RETURN)
    time.sleep(3)
    found_header = driver.find_element(By.CLASS_NAME, "found-header").text
    if found_header != "Found 1 result":
        if found_header == "Found 0 results":
            if not byname:
                return get_vapour_pressures(cas, name, driver,url,byname=True)
            return None, None, None
        driver.find_element(By.CLASS_NAME, "search-list").click()
        time.sleep(1)

    properties_tab = driver.find_element(By.ID, "tab1")
    properties_tab.click()
    time.sleep(1)
    acd_tab = driver.find_element(By.ID, "accordion-acd/labs-title")
    acd_tab.click()
    time.sleep(1)
    vapour_pressure_label = driver.find_element(By.XPATH, '//tr[th[text()="Vapour pressure"]]/td')
    vapour_pressure_value = vapour_pressure_label.text  # Get the text from the corresponding <td>

    mol_name = driver.find_element(By.ID, "cmp-title-label").text
    current_url = driver.current_url
    return mol_name, vapour_pressure_value, current_url

if __name__=="__main__":

    options = webdriver.ChromeOptions()
    options.page_load_strategy = 'normal'
    driver = webdriver.Chrome(options=options)
    url="https://www.chemspider.com/"
    accept_cookies(driver,url)

    print(get_vapour_pressures("25548-04-3","epsilon-Muurolene", driver,url))
    driver.quit()
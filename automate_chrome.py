# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 16:47:46 2023

@author: Abhay Kr Pathak
"""
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import regex as re
from urllib.request import urlretrieve as retrieve
import zipfile
import os
from selenium.webdriver.chrome.service import Service
from urllib.request import urlopen
import json
import warnings
warnings.filterwarnings("ignore")


'''### A method added to download and trigger updated chrome driver and browser respectively ###'''


url='https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json'
response = urlopen(url)
data_json = json.loads(response.read())
INPATH=os.getcwd()+"//"
version=data_json['channels']['Stable']['version']
url='https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/'+version+'/win64/chromedriver-win64.zip'
folder_path=INPATH+version
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Folder '{folder_path}' created successfully.")
    retrieve(url,folder_path+"\\chromedriver-win64.zip")
    for item in os.listdir(folder_path): 
       if item.endswith("zip"): 
           file_namezip = folder_path + "/" + item 
           zip_ref = zipfile.ZipFile(file_namezip) 
           zip_ref.extractall(folder_path) 
           zip_ref.close() 
           os.remove(file_namezip)
else:
    print(f"Folder '{folder_path}' already exists.")

chromepath = folder_path+"\\chromedriver-win64\\chromedriver.exe"

'''             ### Method end ###            '''

service = Service(chromepath)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()
driver.get('https://www.bt.com/')
sleep(3)

# Close accept Cookie pop-up if it appears

try:
    driver.switch_to.frame(0)
    cookies_alert = driver.find_element_by_class_name("mainContent") 
    accept_button=driver.find_element_by_class_name("call") 
    accept_button.click()
    sleep(3)
    driver.switch_to.default_content()
except:
    print('No pop Up for Cokkies')

# Hover to Mobile menu

element1 = driver.find_element_by_xpath('//*[@id="bt-navbar"]/div[2]/div[2]/div/div[1]/div[1]/ul/li[4]/a')
hover = ActionChains(driver).move_to_element(element1).click().perform()

# From mobile menu, select Mobile phones

element2=driver.find_element_by_xpath('//*[@id="bt-navbar"]/div[2]/div[2]/div/div[1]/div[1]/ul/li[4]/ul/li/ul/li[2]/a')
hover = ActionChains(driver).move_to_element(element2).click().perform()
sleep(2)

# Verify the numbers of banners present below “See Handset details” should not be less than 3

try:
    banner1 = driver.find_element_by_xpath('//*[@id="__next"]/div/div[4]/div/div[1]')
    banner2 = driver.find_element_by_xpath('//*[@id="__next"]/div/div[4]/div/div[2]')
    banner3 = driver.find_element_by_xpath('//*[@id="__next"]/div/div[4]/div/div[3]')
    print("All three banners are present on the page.")
except Exception as e:
    print("One or more banners are not present:", e)
    
# Scroll down and click View SIM only deals  

element3 = driver.find_element_by_xpath('//*[@id="__next"]/div/div[5]/div[2]/div[1]/div/div/div/div[2]/div/div[3]/a')  
driver.execute_script("arguments[0].scrollIntoView();", element3)
element3.click()

# Validate the title for new pag 

page_title = driver.title
check_title = "SIM Only Deals"

if re.search(check_title, page_title):
    print(f"The expected text '{check_title}' is found in the page title: '{page_title}'")

# Validate “30% off and double data” was 125GB 250GB Essential Plan, was £27 £18.90 per month

def find_and_validate_text(xpath, expected_text):
    try:
        element = driver.find_element_by_xpath(xpath)
        element_text = element.text
        if re.search(expected_text, element_text):
            print(f"The expected text '{expected_text}' is found in: '{element_text}'")
        else:
            print(f"The expected text '{expected_text}' is not found in: '{element_text}'")
    except Exception as e:
        print(f"An error occurred: {e}")

elements = [
    {"xpath": '//*[@id="__next"]/div/div[4]/div[2]/div/div[2]/div[10]/div[1]', "expected_text": '30% off and double data'},
    {"xpath": '//*[@id="__next"]/div/div[4]/div[2]/div/div[2]/div[10]/div[2]/div[1]/div[1]/span[1]', "expected_text": 'was 125GB'},
    {"xpath": '//*[@id="__next"]/div/div[4]/div[2]/div/div[2]/div[10]/div[2]/div[1]/div[1]/div', "expected_text": '250GB'},
    {"xpath": '//*[@id="__next"]/div/div[4]/div[2]/div/div[2]/div[10]/div[2]/div[1]/div[1]/span[2]', "expected_text": 'Essential Plan'},
    {"xpath": '//*[@id="__next"]/div/div[4]/div[2]/div/div[2]/div[10]/div[2]/div[1]/div[2]/span[1]', "expected_text": 'was £27'},
    {"xpath": '//*[@id="__next"]/div/div[4]/div[2]/div/div[2]/div[10]/div[2]/div[1]/div[2]/div', "expected_text": '£18.90'},
    {"xpath": '//*[@id="__next"]/div/div[4]/div[2]/div/div[2]/div[10]/div[2]/div[1]/div[2]/span[2]', "expected_text": 'Per month'}
]


for element_data in elements:
    find_and_validate_text(element_data["xpath"], element_data["expected_text"])


driver.quit()
    






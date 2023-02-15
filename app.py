#!usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv

load_dotenv()
URL = os.getenv('URL')
USER = os.getenv('USER_URL')
PASS = os.getenv('PASS_URL') 

driver = webdriver.Firefox()
driver.get(URL)

explore_bar = WebDriverWait(driver, 10).until(
EC.presence_of_element_located((By.XPATH, "//a[@id='btnbarraaceptacion']"))
)
explore_bar.click()

username_input =  WebDriverWait(driver, 10).until(
EC.presence_of_element_located((By.XPATH, "//input[@id='login']"))
)
username_input.send_keys(USER)

input_password =  WebDriverWait(driver, 10).until(
EC.presence_of_element_located((By.XPATH, "//input[@id='pass_login']"))
)
input_password.send_keys(PASS)

submit_login_button = WebDriverWait(driver, 10).until(
EC.presence_of_element_located((By.XPATH, "//button[@id='btnLogin']"))
)

submit_login_button.click()
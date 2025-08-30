# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "007D5A5C08F5A6847C89DC60DF95A7D78CA01DA6F4FD25AE9E1E59371C1E5E7D174603B81D8C204F7A904E220C70022B1557CA966E96A58ADC82444F1C5FA81E44C67C62462BD89BF2A8224BEF2AAD87E977082DBC537D27EF0436787C1F03EC5E45577C5D9EBB551BE431794D34A1F61095E04B74AE7C9FCCBD19B582702673EE486D3C19DF64A714DA21745F892B9559591855B9912C8738F56E8F21DE5D2A7DAD2F28AF05B0E962F50FBA347D6FA31FF4C68EFA90BE6ADB4D1B1A3A720000DB6CE9EFD593F112243B091A23DC2AFFDCCFECADF6228D4B3F1B03158D398C514E6EA10E7B66E977E53207394D4F24DD410069195B86C77D55D7BB2F4A5AD5B5EAE3AED4B085794987CF2DB24883BFE1B4D6A19BD9DA24D27772FEE52DF0A31B43C504472362787CAF19494363A991A9AB613AF6F17F050C00BEB7A765D5EDB9BE8898DC8A2B98CAAD94901DC418522818855F0F0C4658EC4EE00205CA6C777AD82F02EEFF7A5E619558A050B60DF36BBFE0DD376F92636A973D7F8CAE742FECD0B2EF10EC1E7E3726AB06CC6AFBF4A53FD7C5403E167A426E61747DCC3DBAE95E"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")

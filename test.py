import os
import time
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import xlrd

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
chromedriver_path = os.path.join(BASE_PATH, "chromedriver")



class Driver(object):
    def __enter__(self):
        self.driver = webdriver.Chrome(executable_path=chromedriver_path)
        self.driver.get('https://pypi.org/project/xlutils/')
        try:
            # WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "side")))
            return self.driver
        except TimeoutException:
            self.driver.quit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


if __name__ == '__main__':
    with Driver() as driver:
        ret = driver.find_elements(By.CSS_SELECTOR, ".vertical-tabs__tab--with-icon.vertical-tabs__tab--is-active")
    print(chromedriver_path)
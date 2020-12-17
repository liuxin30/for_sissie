# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Driver(object):
    def __init__(self, url, executable_path=None, options=None, wait_locator=None):
        """
        :param url:
        :param executable_path:
        :param options:
        :param wait_locator:
        """
        self.url = url
        self.executable_path = executable_path
        self.options = options
        self.wait_locator = wait_locator

    def start(self):
        self.driver = webdriver.Chrome(executable_path=self.executable_path, options=self.options)
        self.driver.get(self.url)
        WebDriverWait(self.driver, 30).until(ec.presence_of_element_located(self.wait_locator))
        return self.driver

    def close(self):
        self.driver.quit()

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# -*- coding: utf-8 -*-
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from read_file import ReadFile
from log import LOG

BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
path = os.path.join(BASE_PATH, "driver")
chromedriver_path = path + "\\chromedriver"
LOG.info("chromedriver path: %s" % chromedriver_path)


class Driver(object):
    def __enter__(self):
        self.driver = webdriver.Chrome(executable_path=chromedriver_path)
        self.driver.get('https://web.whatsapp.com')
        try:
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "side")))
        except TimeoutException:
            self.driver.quit()
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()


class ElementHasTitle(object):
    """An expectation for checking that an element has a particular title.
        locator - used to find the element
        returns the WebElement once it has the particular css class
    """

    def __init__(self, locator, title):
        self.locator = locator
        self.title = title

    def __call__(self, driver):
        element = driver.find_element(*self.locator)  # Finding the referenced element
        if self.title in element.get_attribute("title"):
            return element
        else:
            return False


class WhatsAppPlug(object):
    def __init__(self, driver):
        self.driver = driver

    def search_customer(self, mail_num):
        LOG.info("search customer: %s" % mail_num)
        search_filed = self.driver.find_element_by_xpath(
            "//div[@id='side']/div/div/label/div/div[@class='_3FRCZ copyable-text selectable-text']")
        search_filed.clear()
        search_filed.send_keys(mail_num)
        time.sleep(2)
        conversations = self.driver.find_elements_by_xpath(
            '//*[@id="pane-side"]//div[@class="_210SC"]//span[@class="matched-text _3Whw5"]')
        for conversation in conversations:
            text = conversation.text
            if mail_num in text:
                conversation.click()
                xpath_obj = "//*[@id='main']/header/div[@class='_33QME']/div/div/span"
                WebDriverWait(self.driver, 10).until(ElementHasTitle((By.XPATH, xpath_obj), text))
                return
        raise RuntimeError("未找到%s的对话" % mail_num)

    def send_message(self, messages, image_list):
        LOG.info("send message: %s..." % messages[:2])
        message_filed = self.driver.find_element_by_xpath(
            "//div[@id='main']/footer/div/div[@class='_3uMse']/div/div[@class='_3FRCZ copyable-text selectable-text']")
        message_filed.clear()
        for message in messages:
            message_filed.send_keys(message)
            message_filed.send_keys(Keys.SHIFT + Keys.ENTER)
        message_filed.send_keys(Keys.RETURN)
        time.sleep(2)
        if image_list:
            exten = self.driver.find_element_by_xpath(
                '//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div[@title="附件"]')
            exten.click()
            time.sleep(2)
            image_field = self.driver.find_element_by_xpath(
                "//*[@id='main']/footer//ul[@class='I4jbF']/li[1]/button/input")
            for image in image_list:
                image_field.send_keys(image)
                time.sleep(5)
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "app")))
                self.driver.find_element_by_xpath('//*[@id="app"]//div[@class="_3y5oW _3qMYG"]').click()
        time.sleep(2)


if __name__ == '__main__':
    rf = ReadFile()
    mail_name_dict = rf.get_mail_name_dict()
    message_tmp = rf.get_message()
    image_list = rf.get_images()

    with Driver() as driver:
        wap = WhatsAppPlug(driver)
        fail_list = list()
        for mail, name in mail_name_dict.items():
            try:
                wap.search_customer(mail)
                message = message_tmp.format(name=name)
                messages = message.split('\n')
                wap.send_message(messages, image_list)
            except RuntimeError:
                fail_list.append(mail)
    if fail_list:
        LOG.error(fail_list)

# -*- coding: utf-8 -*-
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
log_path = os.path.join(BASE_PATH, "whatsapp.log")
log_format = "%(asctime)s %(levelname)s: %(message)s"
logging.basicConfig(filename=log_path, level=logging.INFO, format=log_format)
LOG = logging.getLogger(__name__)

chromedriver_path = os.path.join(os.path.dirname(BASE_PATH), "chromedriver")
LOG.info("chromedriver path: %s" % chromedriver_path)


class Driver(object):
    def __enter__(self):
        self.driver = webdriver.Chrome(executable_path=chromedriver_path)
        self.driver.get('https://web.whatsapp.com')
        try:
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "side")))
            return self.driver
        except TimeoutException:
            self.driver.quit()

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


class ReadFile:

    def __init__(self):
        # 联系人信息文件路径
        customer_file_path = os.path.join(BASE_PATH, "customer_file")
        self.customer_info_path = os.path.join(customer_file_path, "customer_info.xlsx")
        LOG.info("customer-info file path: %s" % self.customer_info_path)
        # 自定义消息文件路径
        self.meassge_path = os.path.join(customer_file_path, "message.txt")
        LOG.info("meassge file path: %s" % self.meassge_path)
        # 图片路径
        self.image_path = os.path.join(customer_file_path, "images")
        LOG.info("image path: %s" % self.image_path)

    def get_mail_name_dict(self):
        """
        获取客户邮箱和客户名称的字典
        :return:
        """
        LOG.info("get mail name dict...")
        workbook = xlrd.open_workbook(filename=self.customer_info_path)  # 打开文件
        sheet_obj = workbook.sheet_by_index(0)
        ncows = sheet_obj.nrows
        mail_list = sheet_obj.col_values(0, 1, ncows)
        name_list = sheet_obj.col_values(1, 1, ncows)
        mail_name_dict = dict()
        for i, mail in enumerate(mail_list):
            mail_name_dict[mail] = name_list[i]

        return mail_name_dict

    def get_message(self):
        """
        获取需要发送的消息模板
        :return:
        """
        LOG.info("get message...")
        with open(self.meassge_path, 'r') as f:
            message = f.read()
        return message

    def get_images(self):
        """
        读取图片
        :return:
        """
        image_list = list()
        for image_name in os.listdir(self.image_path):
            (filename, extension) = os.path.splitext(image_name)
            if extension in [".jpg", ".png", ".jpeg"]:
                image_p = os.path.join(self.image_path, image_name)
                image_list.append(image_p)
        return image_list


class WhatsAppPlug(object):
    def __init__(self, driver):
        self.driver = driver

    def search_customer(self, mail_num):
        """
        在搜索栏查找联系人
        :param mail_num:
        :return:
        """
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
        """
        发送消息
        :param messages:
        :param image_list:
        :return:
        """
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
                message = message_tmp.format(name=name.title())
                messages = message.split('\n')
                wap.search_customer(mail)
                wap.send_message(messages, image_list)
            except Exception as e:
                LOG.error(e)
                fail_list.append(mail)
        time.sleep(60*3)
    if fail_list:
        LOG.error("fail_list: %s " % fail_list)

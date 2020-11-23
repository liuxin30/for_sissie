# -*- coding: utf-8 -*-
import os
import sys
import time
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(BASE_PATH)
from utils.wait import wait_until
from utils.file import read_excel, read_txt, write_exist_excel, get_file_path_list
from utils.driver import Driver
from utils.log import log

# whatsapp 项目目录
whatsapp_dir = utils_path = os.path.join(BASE_PATH, "whatsapp")
# 日志设置
log_path = os.path.join(whatsapp_dir, "whatsapp.log")
LOG = log(log_path)

customer_file_dir = os.path.join(whatsapp_dir, "customer_file")
# 联系人信息文件路径
customer_info_path = os.path.join(customer_file_dir, "customer_info.xlsx")
LOG.info("customer info file path: %s" % customer_info_path)
# 自定义消息文件路径
messge_path = os.path.join(customer_file_dir, "message.txt")
LOG.info("meassge file path: %s" % messge_path)
# 图片路径目录
image_dir = os.path.join(customer_file_dir, "images")
LOG.info("image dir: %s" % image_dir)

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')  # 最大化运行（全屏窗口）,不设置，取元素会报错
# chromedriver路径
chromedriver_path = os.path.join(os.path.dirname(whatsapp_dir), "chromedriver")
LOG.info("chromedriver path: %s" % chromedriver_path)


class WhatsAppPlug(object):
    def __init__(self, driver):
        self.driver = driver

    def _is_text_exist(self, locator, text):
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, locator)
            if text in element.text:
                return element
            else:
                return False
        except NoSuchElementException:
            return False

    def search_customer(self, mail_num):
        """
        在搜索栏查找联系人
        :param mail_num:
        :return:
        """
        LOG.info("search customer: %s" % mail_num)
        try:
            search_filed = wait_until(
                lambda: self.driver.find_element(By.CSS_SELECTOR, 'div#side div.copyable-text.selectable-text'))
            search_filed.clear()
            search_filed.send_keys(mail_num)
            time.sleep(2)

            # 等待搜索结果加载完成，并点击，默认搜索结果只有一个
            conversation = wait_until(
                lambda: self._is_text_exist('div#side div[role="option"] span.matched-text', mail_num))
            conversation.click()

            # 等待对话框页面加载完成
            wait_until(lambda: self._is_text_exist('div#main header span[dir="auto"]', mail_num))
            return
        except Exception:
            raise RuntimeError("未找到%s的对话" % mail_num)

    def send_message(self, messages, image_list):
        """
        发送消息
        :param messages:    [list] 需要发送的消息
        :param image_list:  [list] 需要发送图片的列表
        :return:
        """
        LOG.info("send message: %s..." % messages[:2])
        # 查找输送框，发送消息
        message_filed = self.driver.find_element(By.CSS_SELECTOR, 'div#main footer div.copyable-text.selectable-text')
        message_filed.clear()
        for message in messages:
            message_filed.send_keys(message)
            message_filed.send_keys(Keys.SHIFT + Keys.ENTER)
            time.sleep(0.5)
        message_filed.send_keys(Keys.RETURN)
        time.sleep(2)

        # 发送图片
        if image_list:
            for image in image_list:
                # 查找附件按钮
                exten = self.driver.find_element(By.CSS_SELECTOR, 'div#main footer div[title="附件"]')
                exten.click()
                time.sleep(2)

                # 查找发送给图片的输入框
                locator = 'div#main footer input[accept="image/*,video/mp4,video/3gpp,video/quicktime"]'
                image_field = wait_until(lambda: self.driver.find_element(By.CSS_SELECTOR, locator))
                image_field.send_keys(image)
                time.sleep(3)
                send_field = wait_until(
                    lambda: self.driver.find_element(By.CSS_SELECTOR, 'div#app span[data-icon="send"]'))
                send_field.click()
                time.sleep(3)


def main():
    image_list = get_file_path_list(image_dir, ["png", "jpg", "jpeg"])
    message_tmp = read_txt(messge_path)
    values = read_excel(customer_info_path, sheet_index=0, start_row=1, cols=2)
    names = values[0]
    mails = values[1]
    fail_list = list()
    url = "https://web.whatsapp.com/"
    wait_locator = (By.ID, "side")
    with Driver(url, executable_path=chromedriver_path, options=options, wait_locator=wait_locator) as driver:
        wap = WhatsAppPlug(driver)
        for i, mail in enumerate(mails):
            try:
                message = message_tmp.format(name=names[i].title())
                messages = message.strip().split('\n')
                wap.search_customer(mail.strip())
                wap.send_message(messages, image_list)
            except Exception as e:
                LOG.error(e)
                fail_list.append((names[i], mail))
        if fail_list:
            LOG.error("fail_list: %s " % fail_list)
            write_exist_excel(customer_info_path, fail_list, sheet_index=1, start_row=0)
        time.sleep(60 * 3)
    


if __name__ == '__main__':
    main()

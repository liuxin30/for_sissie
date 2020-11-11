import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from get_orders.get_orders.excel_read_write import ExcelReadWrite


def main():
    mail_list = ExcelReadWrite().read()

    # 实例化一个启动参数对象
    chrome_options = Options()
    # 设置浏览器窗口大小
    chrome_options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://thisnew-manager.koniao.com/admin/')
    driver.find_element_by_id('input-username').send_keys("sissie")
    driver.find_element_by_id('password').send_keys("123456")
    driver.find_element_by_id('loginForm').click()
    # # 刷新页面
    # browser.refresh()
    time.sleep(2)

    res = driver.find_element_by_xpath("//ul[@id='menu']/li[@id='menu-sale']/ul[@id='collapse4']/li/a")
    ur = res.get_attribute("href")
    driver.get(ur)
    time.sleep(2)

    info_list = []

    for customer_mail in mail_list:
        mail_form = driver.find_element_by_xpath("//input[@placeholder='用户邮箱']")
        mail_form.clear()
        mail_form.send_keys(customer_mail)
        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(3)

        try:
            orders_date = driver.find_element_by_xpath("//tbody/tr/td/p").text
            orders_num = driver.find_element_by_xpath(
                '//ul[@class="ant-pagination ant-table-pagination"]/li[@class="ant-pagination-total-text"]').text
        except Exception:
            orders_date = ""
            orders_num = ""

        info_list.append((orders_date, orders_num))

    driver.close()
    mail_list.clear()

    with open("info.txt", 'w', encoding="utf-8") as f:
        for i in info_list:
            f.write(str(i) + '\n')


if __name__ == '__main__':
    main()

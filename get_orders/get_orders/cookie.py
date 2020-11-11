# import json
# import time
# from selenium.webdriver.chrome.options import Options
# from selenium import webdriver
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.common.exceptions import NoSuchElementException
#
#
# class Crawler():
#     def gather():
#         chrome_options = Options()
#         chrome_options.add_argument("window-size=1024,768")
#         browser = webdriver.Chrome(chrome_options=chrome_options)
#         wait = WebDriverWait(browser, 1)
#         ##登录
#         logurl = 'https://www.thisnew.com/admin/index.php?route=common/login'
#         # 登录前清楚所有cookie
#         browser.delete_all_cookies()
#         browser.get(logurl)
#         ##登录前打印cookie
#         print(browser.get_cookies())
#
#         ##点击登录按钮
#         usernaem = "sissie"
#         password = "123456"
#         # 通过使用选择器选择到表单元素进行模拟输入和点击按钮提交
#         browser.find_element_by_id('input-username').clear()
#         browser.find_element_by_id('input-username').send_keys(usernaem)
#         browser.find_element_by_id('password').clear()
#         browser.find_element_by_id('password').send_keys(password)  # password
#         browser.find_element_by_id('loginForm').click()
#         time.sleep(2)
#         cookie = browser.get_cookies()
#         print(cookie)
#         jsonCookies = json.dumps(cookie)
#         with open('vcyber.json', 'w') as f:
#             f.write(jsonCookies)
#
#         browser.close()
#
#
# Crawler.gather()

from selenium import webdriver
import pickle

driver = webdriver.Chrome()
driver.get('https://www.thisnew.com/admin/index.php?route=common/dashboard')
driver.find_element_by_id('input-username').send_keys("sissie")
driver.find_element_by_id('password').send_keys("123456")
driver.find_element_by_id('loginForm').click()

# storing the cookies
pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
driver.quit()


# -*- coding: utf-8 -*-
import requests
import os
import time
import logging
import json
import copy

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
log_path = os.path.join(BASE_PATH, "instagram.log")
log_format = "%(asctime)s %(levelname)s: %(message)s"
logging.basicConfig(filename=log_path, level=logging.INFO, format=log_format)
LOG = logging.getLogger(__name__)

BASE_URL = "https://www.instagram.com/graphql/query/?"
HEADERS = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': "zh-CN,zh;q=0.9",
    'referer': 'https://www.instagram.com/printful/followers/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
    'x-csrftoken': 'fiSmQaoHxI7xy6iD7jwwHnLjNzuJR9G9',
    'x-ig-app-id': '936619743392459',
    'x-requested-with': 'XMLHttpRequest',
}

# PROXIES = {
#     'http': 'http://127.0.0.1:1087',
#     'https': 'http://127.0.0.1:1087',
# }

FIRST_PARAMS = {
    "query_hash": "c76146de99bb02f6415203be841dd25a",
    "variables": '{"id":"1426668719","include_reel":true,"fetch_mutual":true,"first":50}'
}

PARAMS = {
    "query_hash": "c76146de99bb02f6415203be841dd25a",
    "variables": '{"id":"1426668719","include_reel":true,"fetch_mutual":true,"first":50,"after":\"%s\"}'
}


class Instagram(object):

    def __init__(self, cookie, csrftoken):
        self.headers = HEADERS
        self.headers.update({"cookie": cookie, "x-csrftoken": csrftoken})

    def get_response(self, end_cursor=None):
        if not end_cursor:
            # response = requests.get(BASE_URL, params=FIRST_PARAMS, headers=self.headers, proxies=PROXIES)
            response = requests.get(BASE_URL, params=FIRST_PARAMS, headers=self.headers)
        else:
            params = copy.copy(PARAMS)
            params["variables"] = params["variables"] % end_cursor
            # response = requests.get(BASE_URL, params=params, headers=self.headers, proxies=PROXIES)
            response = requests.get(BASE_URL, params=params, headers=self.headers)
        return response.text

    def process_data(self, response):
        ret = json.loads(response)
        edge_followed_by = ret["data"]["user"]["edge_followed_by"]
        page_info = edge_followed_by["page_info"]
        end_cursor = page_info.get("end_cursor")
        edges = edge_followed_by["edges"]
        usernames = list()
        for item in edges:
            usernames.append(item["node"]["username"])
        self.write_username(usernames)
        return end_cursor

    def write_username(self, usernames):
        with open("usernames.txt", "a") as f:
            for username in usernames:
                f.write(username + '\n')


if __name__ == '__main__':
    cookies = 'ig_did=960D17BA-B42A-4EDF-AB6C-5E772A00823F; mid=X6VBrAALAAFw8kf5Xx7AXfqY2LSR; ig_nrcb=1; fbm_124024574287414=base_domain=.instagram.com; csrftoken=fiSmQaoHxI7xy6iD7jwwHnLjNzuJR9G9; ds_user_id=7876242157; sessionid=7876242157%3ALY2JycOFaM7PPl%3A17; shbid=17454; shbts=1605423496.7171667; rur=ATN; fbsr_124024574287414=wqNynky-Oy8F0SNBZLHJ8UVvqayCWs1SADCeLpEw-JE.eyJ1c2VyX2lkIjoiMTAwMDI2MzAyMzkwNDk3IiwiY29kZSI6IkFRQnRJM1VYOHJ3RUFXYXVIME1WU3V0b2JMamlleGVONTBvVVBvVWZEbUNNb1E4ekxfMVVBU045OC0xVXZlczJTeXZuQmZYM2dla1hKLUxEaXhBNTRMYXFZTFFzeVRqVkF6X0VIMk1jQmtQR3RzeUMxUGRaRkJJLVlRM1c2RWVOSVZGWUcyOTI1bnNLVHRUNmZZYV9SU1lWUTBqVDUtOUs2RUZ5bVN0b2lrUnpiaWIyN25zQ213VTA2T3hodERqVHlyVlRtSUNIeHEwVEh6NDJYNHdUU2wtdm8wbnZZdFFBOGZpMlc3VWlGTmlYUVVsN3pXaFFhRXk5amwxVWRyNzJpS3VlNGhkcTZjUDRENENMZHRTV25DMHhPNzZBMTY5NVc3SE82ZXFCaGxkMnpraUlsNW1taTR1U2ZrM0dTZWQ1VkQ4Iiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUdRZEd4a0ZaQzhaQzQwTXU1SW15ekliaGpGcXlzRzJoUklaQVJwYlI2d3BaQkdqNGN0ZGI5RXc2Y1U3MmxXcnpMbFpDWkNDNHczTUtqMlpCd0R5MVg4N3VxaE1DVzl5SW4zSDVzS3RXeldKck9iMHFpWkFWbzZoQ1Fzem9oNmJpM3g1TWJaQlR4YlJLdkhkU25uUHZaQzVZV1lsa1lUOE41OFBON0JFYm1JZmtFIiwiYWxnb3JpdGhtIjoiSE1BQy1TSEEyNTYiLCJpc3N1ZWRfYXQiOjE2MDU0NDYzODF9; urlgen="{\"124.108.23.233\": 64271\054 \"45.136.3.9\": 48024}:1keHx2:3kb51R2x8taTZ6yvgd8HtXx-4rQ"'
    csrftoken = "fiSmQaoHxI7xy6iD7jwwHnLjNzuJR9G9"
    cursor = "QVFENVlXc0RCTzhrVlFZS0l6QUlFYW9fZDFVNDlBb2RFd2xOWWprTEp3SGFwbXEwZ2gzU1EtanlTWkVZSFpuM3cydHFnN2JEdGdqN0JrNEZYNDZJR0ZWRA=="
    ins = Instagram(cookies, csrftoken)

    for i in range(100):
    # while cursor:
        print("第%s次。。。" % i)
        try:
            res = ins.get_response(end_cursor=cursor)
        except Exception as e:
            LOG.exception(e)
            res = ins.get_response(end_cursor=cursor)
        cursor = ins.process_data(res)
        LOG.info(cursor)
        time.sleep(2)

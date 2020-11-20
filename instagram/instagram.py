# -*- coding: utf-8 -*-
import requests
import os
import time
import logging
import json
import copy
import re

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
HEADERSS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
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
        self.get_followers_headers = HEADERSS
        self.get_followers_headers.update({"cookie": cookie})

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

    def get_followers(self, username):
        url = "https://www.instagram.com/%s/" % username
        response = requests.get(url, headers=self.get_followers_headers)
        LOG.info("GET: %s, status_code: %s" % (url, response.status_code))
        try:
            ret = re.search(r'meta content="(.+) 位粉丝', response.text)
            followers = ret.group(1)
            if ',' in followers:
                followers = followers.replace(',', '')
            elif 'K' in followers:
                followers = float(followers[:-1]) * 1000
            elif 'M' in followers:
                followers = float(followers[:-1]) * 1000 * 1000
        except Exception as e:
            followers = 0
            LOG.exception(e)

        return {"url": url, "followers": followers}

if __name__ == '__main__':
    cookies = 'ig_did=964BAB54-7E02-4512-8390-C7F53D2873D5; mid=X7UsJAALAAG65F2nNRrXzdRWB4C6; ig_nrcb=1; csrftoken=itCw8LJ0zgOrcvi8iThSGxRYQdlVNi4U; ds_user_id=7876242157; sessionid=7876242157%3AlAtRuGnb6dhKjx%3A7; shbid=17454; shbts=1605708850.732832; rur=ATN; urlgen="{\"124.108.22.102\": 64271}:1kfOT2:i3wd8y-LcMkizQ5GAemfTKNmxF0"'
    csrftoken = "itCw8LJ0zgOrcvi8iThSGxRYQdlVNi4U"
    cursor = "QVFENVlXc0RCTzhrVlFZS0l6QUlFYW9fZDFVNDlBb2RFd2xOWWprTEp3SGFwbXEwZ2gzU1EtanlTWkVZSFpuM3cydHFnN2JEdGdqN0JrNEZYNDZJR0ZWRA=="
    ins = Instagram(cookies, csrftoken)
    ins.get_followers("silvio_luz")

    # for i in range(100):
    # # while cursor:
    #     print("第%s次。。。" % i)
    #     try:
    #         res = ins.get_response(end_cursor=cursor)
    #     except Exception as e:
    #         LOG.exception(e)
    #         res = ins.get_response(end_cursor=cursor)
    #     cursor = ins.process_data(res)
    #     LOG.info(cursor)
    #     time.sleep(2)

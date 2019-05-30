#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from html.parser import HTMLParser
from urllib import request


class LianJiaWangParser (HTMLParser):
    def handle_startendtag(self, tag, attrs):
        print(tag, attrs)

    def handle_data(self, data):
        print(data)


# 公用的 UA
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) " + \
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15"
headers = {'User-Agent': user_agent}

# 先拆分页面数量数据
url = "https://bj.lianjia.com/zufang/"

req = request.Request(url, headers=headers)
response = request.urlopen(req)
content = response.read().decode('utf-8')
parser = LianJiaWangParser()
parser.feed(content)
parser.close()

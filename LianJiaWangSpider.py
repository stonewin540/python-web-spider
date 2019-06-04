#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""入口类（场景类）"""
__author__ = 'stone'

from urllib import request
from LianJiaWangHTMLParser import LianJiaWangItemParser


def start():
    # 公用的 UA
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) " + \
                 "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15"
    headers = {'User-Agent': user_agent}

    # 先拆分页面数量数据
    url = "https://bj.lianjia.com/zufang/"

    req = request.Request(url, headers=headers)
    response = request.urlopen(req)
    content = response.read().decode('utf-8')
    parser = LianJiaWangItemParser()
    parser.feed(content)
    parser.close()
    print('number of pages: %d' % parser.number_of_pages)
    print('---- page 1 parsed ----\n')

    # number_of_pages = parser.number_of_pages
    # number_of_pages = 2
    # if LianJiaWangItemParser.UNKNOWN_PAGE != number_of_pages:
    #     for page in range(2, number_of_pages+1):
    #         page_url = '%spg%d' % (url, page)
    #         page_req = request.Request(page_url, headers=headers)
    #         page_resp = request.urlopen(page_req)
    #         page_content = page_resp.read().decode('utf-8')
    #
    #         page_parser = LianJiaWangItemParser()
    #         page_parser.feed(page_content)
    #         page_parser.close()
    #         print('---- page %d parsed ----\n' % page)


# if __name__ == 'main':
start()

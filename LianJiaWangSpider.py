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

    #
    parser = LianJiaWangItemParser()

    number_of_pages = 1
    page = 1
    while page <= number_of_pages:
        url = "https://bj.lianjia.com/zufang/pg%d" % page
        req = request.Request(url, headers=headers)
        resp = request.urlopen(req)
        content = resp.read().decode('utf-8')

        parser.feed(content)
        parser.close()
        print('pages: %d/%d\n' % (page, number_of_pages))

        page += 1
        # TODO 调试时只想抓取一页数据，非调试模式请打开注释
        # number_of_pages = parser.number_of_pages
        if LianJiaWangItemParser.UNKNOWN_PAGE == number_of_pages:
            number_of_pages = page - 1  # 中断循环


# if __name__ == 'main':
start()

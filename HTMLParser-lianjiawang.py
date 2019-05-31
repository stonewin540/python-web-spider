#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""HTMLParser test for parsing lianjiawang"""

__author__ = "stone"

from html.parser import HTMLParser
from urllib import request


class LianJiaWangParsingCondition(object):
    """LianJiaWangItemParser 解析过程中标示应该解析的字段以及是否正在解析的小模型"""
    def __init__(self, parse_key=None):
        self.parse_key = parse_key
        self.isParsing = False


class LianJiaWangItemParser (HTMLParser):

    # def __init__(self):
    #     super(LianJiaWangItemParser, self).__init__()
    #     self.__main_parsing_condition = LianJiaWangParsingCondition('content__list--item--main')
    #
    #     self.__parsing_conditions = []
    #     self.__parsing_conditions.append(LianJiaWangParsingCondition('content__list--item--title'))
    #     self.__parsing_conditions.append(LianJiaWangParsingCondition('content__list--item--des'))
    #     self.__parsing_conditions.append(LianJiaWangParsingCondition('content__list--item--time'))

    # # 调用顺序如下，比如处理标签 div
    # # tag: a, attrs: [('target', '_blank'), ('href', '/zufang/BJ2194649332370907136.html')]
    # def handle_starttag(self, tag, attrs):
    #     print('handle_starttag')
    #     print('tag:', tag)
    #     print('attrs:', attrs)
    #
    #     if 'div' == tag:
    #         for key, value in attrs:
    #             if 'class' == key:
    #                 if value == self.__main_parsing_condition.parse_key:
    #                     self.__main_parsing_condition.isParsing = True
    #                     print('---- parsing main ----')
    #
    #     if self.__main_parsing_condition.isParsing:
    #         for key, value in attrs:
    #             if 'class' == key:
    #                 for condition in self.__parsing_conditions:
    #                     if str(value).startswith(condition.parse_key):
    #                         condition.isParsing = True

    # data: 整租·苏荷时代 1室1厅 西
    def handle_data(self, data):
        print(self.get_starttag_text())
        # striped = str(data).strip()
        # if self.__main_parsing_condition.isParsing and (len(striped) > 0):
        #     print('handle_data')
        #     print('"', data, '"')
        #     print('end_handle_data')

    # # tag: a
    # def handle_endtag(self, tag):
    #     print('handle_endtag')
    #     print('tag:', tag)
    #
    #     is_subprocess_done = True
    #     for condition in self.__parsing_conditions:
    #         if condition.isParsing:
    #             is_subprocess_done = False
    #             break
    #
    #     if is_subprocess_done and self.__main_parsing_condition.isParsing:
    #         self.__main_parsing_condition.isParsing = False
    #         print('---- parsing main done ----')
    #         print('\n')


class LianJiaWangModle(object):
    """数据模型类"""
    pass


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


if __name__ == '__main__':
    print('it works!')

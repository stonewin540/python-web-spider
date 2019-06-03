#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""HTMLParser test for parsing lianjiawang"""

__author__ = "stone"

from html.parser import HTMLParser
from urllib import request


class LianJiaWangItemParser (HTMLParser):

    MAIN_ATTR_VALUE_KEY = 'content__list--item--main'
    TITLE_ATTR_VALUE_KEY = 'content__list--item--title'
    DES_ATTR_VALUE_KEY = 'content__list--item--des'
    TIME_ATTR_VALUE_KEY = 'content__list--item--time'
    BOTTOM_ATTR_VALUE_KEY = 'content__list--item--bottom'
    PRICE_ATTR_VALUE_KEY = 'content__list--item-price'

    UNKNOWN_PAGE = -1

    # conditions
    def is_in_main_process(self):
        if len(self.attrs_stack) <= 0:
            return False

        is_in = LianJiaWangItemParser.MAIN_ATTR_VALUE_KEY in self.attrs_stack
        return is_in

    def is_in_other_process(self, key=''):
        if not self.is_in_main_process():
            return False
        if len(key) <= 0:
            return False

        last = self.attrs_stack[-1]
        is_in = last == key
        return is_in

    def model_in_process(self):
        if self.model is None:
            self.model = LianJiaWangModle()
        return self.model

    # data refreshing
    def append_attr_value_if_possible(self, value, attr_value, tag):
        value_str = str(value)
        found = -1 != value_str.find(attr_value)
        if found:
            self.attrs_stack.append(attr_value)
            self.tags_stack.append(tag)

    def append_with_tag_attrs_if_possible(self, tag, attrs):
        for key, value in attrs:
            # title
            self.append_attr_value_if_possible(value, LianJiaWangItemParser.TITLE_ATTR_VALUE_KEY, tag)
            # des
            self.append_attr_value_if_possible(value, LianJiaWangItemParser.DES_ATTR_VALUE_KEY, tag)
            # time
            self.append_attr_value_if_possible(value, LianJiaWangItemParser.TIME_ATTR_VALUE_KEY, tag)
            self.append_attr_value_if_possible(value, LianJiaWangItemParser.BOTTOM_ATTR_VALUE_KEY, tag)
            self.append_attr_value_if_possible(value, LianJiaWangItemParser.PRICE_ATTR_VALUE_KEY, tag)

    def refresh_model_with_data(self, data):
        striped = str(data).strip()
        if len(striped) > 0:
            # if self.is_in_other_process(LianJiaWangItemParser.TITLE_ATTR_VALUE_KEY):
            #     title = '%s %s' % (self.model_in_process().title, striped)
            #     self.model_in_process().title = title
            #
            # if self.is_in_other_process(LianJiaWangItemParser.DES_ATTR_VALUE_KEY):
            #     des = '%s %s' % (self.model_in_process().des, striped)
            #     self.model_in_process().des = des
            #
            # if self.is_in_other_process(LianJiaWangItemParser.TIME_ATTR_VALUE_KEY):
            #     time = '%s %s' % (self.model_in_process().time, striped)
            #     self.model_in_process().time = time

            # if self.is_in_other_process(LianJiaWangItemParser.TITLE_ATTR_VALUE_KEY):
            #     self.refresh_model(striped, LianJiaWangItemParser.TITLE_ATTR_VALUE_KEY)
            #
            # if self.is_in_other_process(LianJiaWangItemParser.DES_ATTR_VALUE_KEY):
            #     self.refresh_model(striped, LianJiaWangItemParser.DES_ATTR_VALUE_KEY)
            #
            # if self.is_in_other_process(LianJiaWangItemParser.TIME_ATTR_VALUE_KEY):
            #     self.refresh_model(striped, LianJiaWangItemParser.TIME_ATTR_VALUE_KEY)
            #
            # if self.is_in_other_process(LianJiaWangItemParser.BOTTOM_ATTR_VALUE_KEY):
            #     self.refresh_model(striped, LianJiaWangItemParser.BOTTOM_ATTR_VALUE_KEY)
            #
            # if self.is_in_other_process(LianJiaWangItemParser.PRICE_ATTR_VALUE_KEY):
            #     self.refresh_model(striped, LianJiaWangItemParser.PRICE_ATTR_VALUE_KEY)

            attr_value_keys = [LianJiaWangItemParser.TITLE_ATTR_VALUE_KEY,
                               LianJiaWangItemParser.DES_ATTR_VALUE_KEY,
                               LianJiaWangItemParser.TIME_ATTR_VALUE_KEY,
                               LianJiaWangItemParser.BOTTOM_ATTR_VALUE_KEY,
                               LianJiaWangItemParser.PRICE_ATTR_VALUE_KEY]
            for attr_value_key in attr_value_keys:
                if self.is_in_other_process(attr_value_key):
                    self.refresh_model(striped, attr_value_key)

    def refresh_model(self, striped, attr_value_key):
        model = self.model_in_process()
        for property_name in dir(model):
            mixed_name = 'content__list--item--%s' % property_name
            if mixed_name != attr_value_key:
                mixed_name = 'content__list--item-%s' % property_name

            if mixed_name == attr_value_key:
                new_value = '%s %s' % (getattr(model, property_name), striped)
                setattr(model, property_name, new_value)

    def __init__(self):
        super(LianJiaWangItemParser, self).__init__()
        self.attrs_stack = []
        self.tags_stack = []
        self.model = None
        self.models = []
        self.number_of_pages = LianJiaWangItemParser.UNKNOWN_PAGE

    # # 调用顺序如下，比如处理标签 div
    # # tag: a, attrs: [('target', '_blank'), ('href', '/zufang/BJ2194649332370907136.html')]
    def handle_starttag(self, tag, attrs):
        if ('div' == tag) and (not self.is_in_main_process()):
            is_main = False
            for attr in attrs:
                if len(attr) > 1:
                    value = attr[1]
                    if value == LianJiaWangItemParser.MAIN_ATTR_VALUE_KEY:
                        is_main = True
                        break
            if is_main:
                self.attrs_stack.append(LianJiaWangItemParser.MAIN_ATTR_VALUE_KEY)
                self.tags_stack.append(tag)
                print('---- parsing main ----')

        if self.is_in_main_process():
            self.append_with_tag_attrs_if_possible(tag, attrs)

        if (LianJiaWangItemParser.UNKNOWN_PAGE == self.number_of_pages) and ('div' == tag):
            for key, value in attrs:
                if 'data-totalpage' == key:
                    self.number_of_pages = int(value)
                    break

    # data: 整租·苏荷时代 1室1厅 西
    def handle_data(self, data):
        self.refresh_model_with_data(data)

    # tag: a
    def handle_endtag(self, tag):
        if (len(self.tags_stack) > 0) and (tag == self.tags_stack[-1]):
            poped_attr = self.attrs_stack.pop()
            poped_tag = self.tags_stack.pop()
            if LianJiaWangItemParser.MAIN_ATTR_VALUE_KEY == poped_attr:
                print(self.model)
                self.models.append(self.model)
                self.model = None
                print('number of models:', len(self.models))
                print('---- parsing main done ----')
                print('\n')


class LianJiaWangModle(object):
    """数据模型类"""
    def __init__(self):
        self.title = ''
        self.des = ''
        self.time = ''
        """命名 bottom 是为了跟 HTML 代码中的名字保持一致并方便批量赋值；但其实的意义是 features"""
        self.bottom = ''
        self.price = ''

    def __str__(self):
        return '%8s: %s\n' \
               '%8s: %s\n' \
               '%8s: %s\n' \
               '%8s: %s\n' \
               '%8s: %s' % \
               ('title', self.title,
                'des', self.des,
                'time', self.time,
                'bottom', self.bottom,
                'price', self.price)
    __repr__ = __str__


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
print('---- page 1 parsed ----\n')

number_of_pages = parser.number_of_pages
number_of_pages = 2
if LianJiaWangItemParser.UNKNOWN_PAGE != number_of_pages:
    for page in range(2, number_of_pages+1):
        page_url = '%spg%d' % (url, page)
        page_req = request.Request(page_url, headers=headers)
        page_resp = request.urlopen(page_req)
        page_content = page_resp.read().decode('utf-8')

        page_parser = LianJiaWangItemParser()
        page_parser.feed(page_content)
        page_parser.close()
        print('---- page %d parsed ----\n' % page)


# if __name__ == '__main__':
#     print('it works!')

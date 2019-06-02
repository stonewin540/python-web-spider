#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""HTMLParser test for parsing lianjiawang"""

__author__ = "stone"

from html.parser import HTMLParser
from urllib import request


class LianJiaWangItemParser (HTMLParser):

    MAIN_ATTR_KEY = 'content__list--item--main'
    TITLE_ATTR_KEY = 'content__list--item--title'
    DES_ATTR_KEY = 'content__list--item--des'

    def is_in_main_process(self):
        if len(self.attrs_stack) <= 0:
            return False

        is_in = LianJiaWangItemParser.MAIN_ATTR_KEY in self.attrs_stack
        return is_in

    def is_in_main_title_process(self):
        if not self.is_in_main_process():
            return False

        last = self.attrs_stack[-1]
        return LianJiaWangItemParser.TITLE_ATTR_KEY == last

    def is_in_main_des_process(self):
        if not self.is_in_main_process():
            return False
        last = self.attrs_stack[-1]
        return LianJiaWangItemParser.DES_ATTR_KEY == last

    def model_in_process(self):
        if self.model is None:
            self.model = LianJiaWangModle()
        return self.model

    def __init__(self):
        super(LianJiaWangItemParser, self).__init__()
        self.attrs_stack = []
        self.tags_stack = []
        self.model = None
        self.models = []

    # # 调用顺序如下，比如处理标签 div
    # # tag: a, attrs: [('target', '_blank'), ('href', '/zufang/BJ2194649332370907136.html')]
    def handle_starttag(self, tag, attrs):
        if ('div' == tag) and (not self.is_in_main_process()):
            is_main = False
            for attr in attrs:
                if len(attr) > 1:
                    value = attr[1]
                    if value == LianJiaWangItemParser.MAIN_ATTR_KEY:
                        is_main = True
                        break
            if is_main:
                self.attrs_stack.append(LianJiaWangItemParser.MAIN_ATTR_KEY)
                self.tags_stack.append(tag)
                print('---- parsing main ----')

        if self.is_in_main_process():
            for key, value in attrs:
                value_str = str(value)
                # title
                is_title = -1 != value_str.find(LianJiaWangItemParser.TITLE_ATTR_KEY)
                if is_title:
                    self.attrs_stack.append(LianJiaWangItemParser.TITLE_ATTR_KEY)
                    self.tags_stack.append(tag)

                # des
                is_des = -1 != value_str.find(LianJiaWangItemParser.DES_ATTR_KEY)
                if is_des:
                    self.attrs_stack.append(LianJiaWangItemParser.DES_ATTR_KEY)
                    self.tags_stack.append(tag)

    # data: 整租·苏荷时代 1室1厅 西
    def handle_data(self, data):
        striped = str(data).strip()
        if len(striped) > 0:
            if self.is_in_main_title_process():
                title = '%s %s' % (self.model_in_process().title, striped)
                self.model_in_process().title = title

            if self.is_in_main_des_process():
                des = '%s %s' % (self.model_in_process().des, striped)
                self.model_in_process().des = des

    # # tag: a
    def handle_endtag(self, tag):
        if (len(self.tags_stack) > 0) and (tag == self.tags_stack[-1]):
            poped_attr = self.attrs_stack.pop()
            poped_tag = self.tags_stack.pop()
            if LianJiaWangItemParser.MAIN_ATTR_KEY == poped_attr:
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
        self.features = ''
        self.price = ''

    def __str__(self):
        return 'title: %s, des: %s' % (self.title, self.des)
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


if __name__ == '__main__':
    print('it works!')

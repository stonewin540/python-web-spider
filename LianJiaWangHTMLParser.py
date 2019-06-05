#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""HTMLParser test for parsing lianjiawang"""

__author__ = "stone"

from html.parser import HTMLParser
from LianJiaWangModel import LianJiaWangModel


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
            self.model = LianJiaWangModel()
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
        if self.is_in_other_process(LianJiaWangItemParser.TITLE_ATTR_VALUE_KEY):
            self.model_in_process().set_href_with_starttag(self.get_starttag_text())

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





# if __name__ == '__main__':
#     print('it works!')

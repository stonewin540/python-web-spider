#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""数据模型"""
__author__ = 'stone'

import re
import LianJiaWangConfig


class LianJiaWangModel(object):
    def __init__(self):
        self.title = ''
        self.des = ''
        self.time = ''
        """命名 bottom 是为了跟 HTML 代码中的名字保持一致并方便批量赋值；但其实的意义是 features"""
        self.bottom = ''
        self.price = ''
        self.__href = ''

    def __str__(self):
        return '%8s: %s\n' \
               '%8s: %s\n' \
               '%8s: %s\n' \
               '%8s: %s\n' \
               '%8s: %s\n' \
               '%8s:  %s\n' % \
               ('title', self.title,
                'des', self.des,
                'time', self.time,
                'bottom', self.bottom,
                'price', self.price,
                'href', self.href())
    __repr__ = __str__

    def set_href_with_starttag(self, starttag):
        striped = str(starttag).strip()
        if len(striped) > 0:
            pattern = re.compile('href="(.+?)"')
            result = re.findall(pattern, striped)
            # 匹配了多条结果肯定也是有问题的
            if len(result) == 1:
                self.__href = str(result[0])
                self.__href = self.__href.replace('/', '', 1)

    def href(self):
        return LianJiaWangConfig.BASE_URL + self.__href

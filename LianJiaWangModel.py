#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""数据模型"""
__author__ = 'stone'


class LianJiaWangModel(object):
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

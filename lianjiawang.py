# coding=utf-8
# import urllib
import urllib2
import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 公用的 UA
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) " + \
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15"
headers = {'User-Agent': user_agent}

# 先拆分页面数量数据
url = "https://bj.lianjia.com/zufang/"
try:
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    content = response.read().decode('utf-8')
    # content__pg
    pg_pattern = re.compile(r'<div class="content.*?>(.*?)</div>', re.S)
    pg_results = re.findall(pg_pattern, content)
    for pg_result in pg_results:
        print(pg_result)
        # a_href_pattern = re.compile("<a href.*?>(.*?)</a>", re.S)
        # a_href_results = re.findall(a_href_pattern, pg_result)
        # for a_href_result in a_href_results:
        #     number_of_pages = a_href_result.strip()
        #     print(number_of_pages)
except urllib2.URLError, e:
    print(e)

# 根据页面数量，逐页爬取
page = 1
url_pg = 'https://bj.lianjia.com/zufang/pg' + str(page)
try:
    request_pg = urllib2.Request(url_pg, headers=headers)
    response_pg = urllib2.urlopen(request_pg)
    content_pg = response_pg.read().decode('utf-8')
    # 匹配整条数据先
    main_pattern = re.compile("<div.*?content__list--item--main.*?>(.*?)</div>", re.S)
    main_results = re.findall(main_pattern, content_pg)
    for main_result in main_results:
        print("---- an item ----")

        # 匹配 title
        title_pattern = re.compile("<p.*?content__list--item--title.*?>(.*?)</p>", re.S)
        title_results = re.findall(title_pattern, main_result)
        for title_result in title_results:
            title_a_pattern = re.compile("<a.*?>(.*?)</a>", re.S)
            title_a_results = re.findall(title_a_pattern, title_result)
            for title_a_result in title_a_results:
                print(title_a_result.strip())

        # 匹配 des
        des_pattern = re.compile("<p.*?content__list--item--des.*?>(.*?)</p>", re.S)
        des_results = re.findall(des_pattern, main_result)
        for des_result in des_results:
            # tag a
            des_a_pattern = re.compile("<a.*?>(.*?)</a>", re.S)
            des_a_results = re.findall(des_a_pattern, des_result)
            for des_a_result in des_a_results:
                print(des_a_result.strip())

            # tag i
            des_i_pattern = re.compile("i>([^/]*?)<", re.S)
            des_i_results = re.findall(des_i_pattern, des_result)
            for des_i_result in des_i_results:
                print(des_i_result.strip())

        # 匹配 time
        time_pattern = re.compile("<p.*?content__list--item--time.*?>(.*?)</p>", re.S)
        time_results = re.findall(time_pattern, main_result)
        for time_result in time_results:
            print(time_result.strip())

        # 匹配 price
        price_pattern = re.compile("<span.*?content__list--item-price.*?>(.*?)</span>", re.S)
        price_results = re.findall(price_pattern, main_result)
        for price_result in price_results:
            price_em_pattern = re.compile("</*em>", re.S)
            price_em_subbed = re.sub(price_em_pattern, "", price_result.strip())
            print(price_em_subbed)

        print("---- end item ----")
except urllib2.URLError, e:
    print e


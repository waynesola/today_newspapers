#!/usr/bin/python
# coding:utf-8

import scrapy
from bs4 import BeautifulSoup
import urlparse
from ..items import TodayNewspapersItem


class AllArticles(scrapy.Spider):
    name = "sztqb"
    allowed_domains = ["sznews.com"]
    start_urls = [
        "http://sztqb.sznews.com"
    ]

    # 爬取指定天数的报纸
    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, "html5lib")
        ts = soup.find('div', attrs={"style": "height:730px; overflow-y:scroll; width:100%;"}) \
            .find_all('table',
                      width="100%",
                      border="0",
                      cellspacing="1",
                      cellpadding="0")
        for t in ts:
            als = t.find('table', cellspacing="0", cellpadding="1", border="0").tbody.find_all('a')
            for al in als:
                item = TodayNewspapersItem()
                if (al.div.get_text() != u"广告") & (al.div.get_text() != u"今日天气") & (al.div.get_text() != u"公告"):
                    item['title'] = al.div.get_text()
                    # 根据当前url（当天首页）和文章相对路径，补全绝对路径
                    link = urlparse.urljoin(response.url, al.get('href'))
                    item['link'] = link
                    # publish = soup.find('table', id="logoTable") \
                    #     .find('td', width="204", align="center", valign="top").get_text()
                    publish = u"深圳特区报"
                    item['publish'] = publish
                    request_article = scrapy.Request(link, callback=self.parse_article)
                    # 不同parse()之间传递item值需要meta['item']
                    request_article.meta['item'] = item
                    yield request_article

    # 爬取某一篇文章正文内容
    def parse_article(self, response):
        item = response.meta['item']
        data = response.body
        soup = BeautifulSoup(data, "html5lib")
        text = ""
        ts = soup.find('div', style="height:900px; overflow-y:scroll; width:100%;").find('tbody').find_all('tr',
                                                                                                           valign='top')
        temp = "    "
        for t in ts:
            if t.get_text() is not None:
                temp += t.get_text() + '\n\n    '
        text += temp
        ps = soup.find('founder-content').find_all('p')
        for p in ps:
            text += p.get_text()
            text += "\n\n    "
        item['text'] = text
        publish = item["publish"]
        pub = soup.find("table", width=413, border=0, cellpadding=5, cellspacing=0, style="MARGIN-BOTTOM: 3px") \
            .find("strong")
        publish += "  " + pub.parent.get_text()
        item["publish"] = publish
        yield item

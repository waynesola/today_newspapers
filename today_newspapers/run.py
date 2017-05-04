#!/usr/bin/python
# coding:utf-8

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl('sztqb')
process.crawl('rmrb')
process.crawl('nfrb')
process.start()  # the script will block here until the crawling is finished

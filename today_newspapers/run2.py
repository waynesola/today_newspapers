#!/usr/bin/python
# coding:utf-8

'''
Run this script with command 'python run2.py'
'''

import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

configure_logging()
runner = CrawlerRunner(get_project_settings())
runner.crawl('sztqb')
runner.crawl('rmrb')
runner.crawl('nfrb')
d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()  # the script will block here until all crawling jobs are finished

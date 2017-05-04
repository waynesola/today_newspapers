# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from items import TodayNewspapersItem


class TodayNewspapersPipeline(object):
    def process_item(self, item, spider):
        if item.__class__ == TodayNewspapersItem:  # 此句非必要，在多个items时可能需要用到
            conn = sqlite3.connect('C:/Program Files/DB Browser for SQLite/database/database.db')
            cur = conn.cursor()
            # SQLite的placeholder是问号[?]，非[%s]。
            # 表名是today_newspapers，表名不能为纯数字！
            sql = "insert into today_newspapers(title,publish,link,text) values (?,?,?,?)"
            # 此处最后的逗号[,]不能少
            cur.execute(sql, (item['title'], item['publish'], item['link'], item['text'],))
            conn.commit()
            cur.close()
            conn.close()

        return item

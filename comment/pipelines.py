# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from comment.items import CommentItem,WeiboItem,WeiboCommentItem
# import re


class CommentPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,WeiboCommentItem):
            if len(item["commentText"]) > 255:
                item["commentText"] = item["commentText"][:50]
            # result = re.search('q:(.*)\|',item['itemid'])
            # if result.group(1)[0] == "#":
            #     item["itemid"] = result.group(1).replace("#","")
            # else:
            #     item["itemid"] = result.group(1)
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            password = '024270',
            db = 'comment',
            charset = 'utf8mb4'
        )
        self.cursor= self.connect.cursor()


    def process_item(self,item,spider):
        if isinstance(item,CommentItem):
            insert_sql = "INSERT INTO comment(hostname,desc_num) VALUES ('%s','%s')" % (item['hostname'],item['desc_num'])
            self.cursor.execute(insert_sql)
            self.connect.commit()
        if isinstance(item,WeiboItem):
            insert_sql1 = "INSERT INTO Weiboitem(screen_name,verified_reason,comments_count,attitudes_count,reposts_count,k_hostname) VALUES ('%s','%s','%s','%s','%s','%s')" % (item["screen_name"],item["verified_reason"],item["comments_count"],item["attitudes_count"],item["reposts_count"],item["hostname"])
            self.cursor.execute(insert_sql1)
            self.connect.commit()
        if isinstance(item,WeiboCommentItem):
            insert_sql2 = "INSERT INTO Weibocommentitem(user,commentText,c_screen_name) VALUES ('%s','%s','%s')" % (item["user"],pymysql.escape_string(item["commentText"]),item["screen_name"])
            self.cursor.execute(insert_sql2)
            self.connect.commit()
        return item


    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()

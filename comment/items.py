# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

# ******微博热搜内容******
class CommentItem(Item):
    hostname = Field()   # 热搜
    desc_num = Field()   # 热度

class WeiboItem(Item):
    hostname = Field()  # 热搜内容
    text = Field()   # 微博内容
    reposts_count = Field()   # 转发数量
    comments_count = Field()  # 评论数量
    attitudes_count = Field() # 赞数
    id = Field()  # ID
    verified_reason = Field()  # 用户所属
    screen_name = Field()      # 用户名字
class WeiboCommentItem(Item):
    user = Field()     # 用户名字
    commentText = Field() # 评论内容
    screen_name = Field() # 用户名字
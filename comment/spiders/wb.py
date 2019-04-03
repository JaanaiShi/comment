# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider
import json
from ..items import CommentItem,WeiboItem,WeiboCommentItem
import requests

class WbSpider(CrawlSpider):

    name = 'wb'
    allowed_domains = ['m.weibo.cn']
    start_urls = ['https://m.weibo.cn/']
    hot_url = "https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C&extparam=filter_type%3Drealtimehot%26mi_cid%3D100103%26pos%3D0_0%26c_type%3D30%26display_time%3D1551943042&luicode=10000011&lfid=231583"
    url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D60%26q%3D%23{}%23&page={}"

    def start_requests(self):
        yield Request(url=self.hot_url,callback=self.parse_weibo,dont_filter=False)

    def parse_weibo(self,response):
        global hostname
        item =  CommentItem()
        # 获得大模块
        data_lists = json.loads(response.text).get("data").get("cards")[0].get("card_group")
        for data in data_lists:
            # 爬取热搜关键字
            hostname = data.get("desc")
            item["hostname"] = hostname
            # 爬取热搜的数量

            item["desc_num"] = data.get("desc_extr")
            yield item


            for i in range(20):
                r = requests.get(url=self.url.format(hostname,i),verify=False)
                # try:
                #     print(len(json.loads(r.text).get("data").get("cards")))
                # except json.JSONDecodeError:
                #     continue
                try:
                    if len(json.loads(r.text).get("data").get("cards")) == 0:
                        break
                except json.decoder.JSONDecodeError:
                    continue

                    # 抓取热门微博
                yield Request(url=self.url.format(hostname,i),callback=self.parse_first,dont_filter=False)


    def parse_first(self,response):

        global screen_name
        item = WeiboItem()
        #使用json解析,获得大模块
        # print(response.text)
        data_list = json.loads(response.text).get("data").get("cards")[0].get("card_group")
        # print(data_list)
        for data in data_list:
            # item["itemid"] = data.get("itemid")
            screen_name = data.get("mblog").get("user").get("screen_name")
            item["screen_name"] = screen_name
            item["verified_reason"] = data.get("mblog").get("user").get("verified_reason")
            item["comments_count"] = data.get("mblog").get("comments_count")
            item["attitudes_count"] = data.get("mblog").get("attitudes_count")
            item["reposts_count"] = data.get("mblog").get("reposts_count")
            item["hostname"] = hostname
            yield item
            # 微博评论的网址的id
            id = data.get("mblog").get("id")
            url = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0".format(id, id)
            yield Request(url=url,callback=self.parse_comment)

    # 对微博评论的解析
    def parse_comment(self,response):
        item = WeiboCommentItem()
        try:
            data_list = json.loads(response.text).get("data").get("data")
            for data in data_list:
                user = data.get("user").get("screen_name")
                # 微博评论者
                item["user"] = user
                item["screen_name"] = screen_name
                commentText = data.get("text")
                if len(commentText) > 50:
                    commentText = commentText[:50]
                # 微博评论内容
                item["commentText"] = commentText
                # print("知名用户:{}：内容:{}".format(user,commentText))
                yield item
        except TypeError as t:
            print("Error",t)
        except AttributeError as a:
            print("Error",a)

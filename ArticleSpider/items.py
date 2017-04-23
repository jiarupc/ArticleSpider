# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    create_date = scrapy.Field()  # 创建日期
    url = scrapy.Field()  # 文章 url
    url_object_id = scrapy.Field()
    front_img_url = scrapy.Field()  # 图片 url
    front_img_path = scrapy.Field()  # 图片路径
    praise_nums = scrapy.Field()  # 点赞数
    fav_nums = scrapy.Field()  # 收藏数
    comment_nums = scrapy.Field()  # 评论数
    tags = scrapy.Field()  # 文章标签
    content = scrapy.Field()  # 正文
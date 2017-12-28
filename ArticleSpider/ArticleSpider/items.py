# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import datetime
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# class ArticleItemLoader(ItemLoader):
#     # 自定义itemloader
#     default_output_processor = TakeFirst()
#
#
# def date_convert(value):
#     try:
#         create_date = datetime.datetime.strptime(value, '%Y/%m/%d').date()
#     except Exception as e:
#         create_date = datetime.datetime.now().date()
#     return create_date
#
#
# def return_value(value):
#     return value
#
#
# def get_nums(value):
#     match_re = re.match(r'.*?(\d+).*', value)
#     if match_re:
#         nums = int(match_re.group(1))
#     else:
#         nums = 0
#
#     return nums
#
#
# def remove_comment_tags(value):
#     if '评论' in value:
#         return ''
#     else:
#         return value


class JobBoleArticleItem(scrapy.Item):
    # title = scrapy.Field()
    # create_date = scrapy.Field(
    #     input_processor=MapCompose(date_convert),
    # )
    # url = scrapy.Field()
    # url_object_id = scrapy.Field()
    # front_image_url = scrapy.Field(
    #     output_processor=MapCompose(return_value),
    # )
    # front_image_path = scrapy.Field()
    # tags = scrapy.Field(
    #     input_processor=MapCompose(remove_comment_tags),
    #     output_processor=Join(','),
    # )
    # post_nums = scrapy.Field(
    #     input_processor=MapCompose(get_nums),
    # )
    # fav_nums = scrapy.Field(
    #     input_processor=MapCompose(get_nums),
    # )
    # comment_nums = scrapy.Field(
    #     input_processor=MapCompose(get_nums),
    # )
    # comments = scrapy.Field()
    # content = scrapy.Field()

    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    tags = scrapy.Field()
    post_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    comments = scrapy.Field()
    content = scrapy.Field()

    # def get_insert_sql(self):
    #     insert_sql = """
    #         insert into jobbolearticle(title, url, create_date, fav_nums, front_image_url, front_image_path,
    #         post_nums, comment_nums, tags, comments, content)
    #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE content=VALUES(fav_nums)
    #     """
    #
    #     fron_image_url = ""
    #
    #     if self["front_image_url"]:
    #         fron_image_url = self["front_image_url"][0]
    #     params = (self["title"], self["url"], self["create_date"], self["fav_nums"],
    #               fron_image_url, self["front_image_path"], self["post_nums"], self["comment_nums"],
    #               self["tags"], self['comments'], self["content"])
    #     return insert_sql, params
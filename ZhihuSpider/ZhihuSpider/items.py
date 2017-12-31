# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy
import time


class ZhihuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ZhihuAnswerItem(scrapy.Item):
    answer_id = scrapy.Field()
    author_id = scrapy.Field()
    author_name = scrapy.Field()
    created_time = scrapy.Field()
    updated_time = scrapy.Field()
    question_title = scrapy.Field()
    question_id = scrapy.Field()
    voteup_count = scrapy.Field()
    comment_count = scrapy.Field()
    content = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                           insert into zhihuanswer(answer_id, author_id, author_name, created_time,
                           updated_time, question_title, question_id, voteup_count, comment_count, content, crawl_time) VALUES (
                           %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                       """

        params = (self['answer_id'], self['author_id'], self['author_name'], self['created_time'], self['updated_time'],
                  self['question_title'], self['question_id'], self['voteup_count'], self['comment_count'],
                  self['content'], self['crawl_time'])
        return insert_sql, params
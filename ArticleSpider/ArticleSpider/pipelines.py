# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

import MySQLdb
import MySQLdb.cursors

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义导出json文件
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    # 调用scrapy提供的json_export到处json文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item()
        return item


class MysqlPipeline(object):
    # 同步存储
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'zhanshi123', 'jobbolearticle_spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
                    insert into jobbolearticle(title, url, create_date, fav_nums, front_image_url, front_image_path,
                    post_nums, comment_nums, tags, comments, content, url_object_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

        fron_image_url = ""

        if item["front_image_url"]:
            fron_image_url = item["front_image_url"][0]
        params = (item["title"], item["url"], item["create_date"], item["fav_nums"],
                  fron_image_url, item["front_image_path"], item["post_nums"], item["comment_nums"],
                  item["tags"], item['comments'], item["content"], item['url_object_id'])
        self.cursor.execute(insert_sql, params)
        self.conn.commit()


class MysqlTwistedPipeline(object):
    """
    创建异步存储数据
    """
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)# 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 具体的数据插入操作
        insert_sql = """
            insert into jobbolearticle(title, url, create_date, fav_nums, front_image_url, front_image_path,
            post_nums, comment_nums, tags, comments, content)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE content=VALUES(fav_nums)
        """

        fron_image_url = ""

        if item["front_image_url"]:
            fron_image_url = item["front_image_url"][0]
        params = (item["title"], item["url"], item["create_date"], item["fav_nums"],
                  fron_image_url, item["front_image_path"], item["post_nums"], item["comment_nums"],
                  item["tags"], item['comments'], item["content"])
        cursor.execute(insert_sql, params)


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if 'front_image_url' in item:
            for ok, value in results:
                image_file_path = value['path']
            item['front_image_path'] = image_file_path
        return item
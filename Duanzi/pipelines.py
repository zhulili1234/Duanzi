# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from MySQLdb.cursors import DictCursor
from twisted.enterprise import adbapi
import MySQLdb

class DuanziPipeline(object):
    def process_item(self, item, spider):
        return item


class MyImgPipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        print results
        path = ""
        for result in results:
            path += result[1]['path']
            path += ","

        item['path'] = path

        print path
        return item

#python2.7 安装mysql驱动  找一个mysql-python.exe 双击安装
#Python2.7 虚拟环境装驱动 拷贝两个以mysql开头的文件夹 _mysql 开头的白色文件到虚拟环境的site-packages
#python3.x pip install mysqlclient

class MySqlPipeline(object):
    @classmethod
    def from_settings(cls, settings):
        # pool:池子
        # con:连接
        # 参数1:dbapiName 数据库接口名称,
        # 参数2: *connargs  *args
        # 参数3: **connkw   **kwargs
        config = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USERNAME'],
            passwd=settings['MYSQL_PASSWORD'],
            db=settings['MYSQL_DB'],
            use_unicode=True,
            charset=settings['MYSQL_CHARSET'],
            cursorclass=DictCursor,
            port=settings['MYSQL_PORT']
        )
        dbpool = adbapi.ConnectionPool(
            "MySQLdb",
            **config
        )
        # 把传递的参数给__init__
        return cls(dbpool)

    def __init__(self, dbpool):
        self.dbpool = dbpool
        # query = self.dbpool.runInteraction(self.drop_table)
        # query.addErrback(self.insert_err)
        query = self.dbpool.runInteraction(self.create_table)
        query.addErrback(self.insert_err)

    def create_table(self, cursor):
        sql = "create table if not exists duanzi (id INT PRIMARY KEY auto_increment NOT NULL ,text longtext ,digg_count  INT DEFAULT 0,bury_count  INT DEFAULT 0 ,repin_count INT DEFAULT 0,comment_count INT DEFAULT 0,path longtext, `type` VARCHAR (10))"
        cursor.execute(sql)

    def process_item(self, item, spider):
        #将Item存到数据库
        query = self.dbpool.runInteraction(self.insert_sql, item)
        # 当执行过程当中出现错误,会执行errback中的方法
        query.addErrback(self.insert_err)
        return item

    def insert_err(self, failed):
        print ">>>>>>>>>>>>>>>>>>>>", failed

    def insert_sql(self, cursor, item):
        sql = "insert into duanzi (text,digg_count,bury_count,repin_count,comment_count,path,`type`) values (%s,%s,%s,%s,%s, %s, %s)"
        cursor.execute(sql, (
            item['text'], item['digg_count'], item['bury_count'],
            item['repin_count'], item['comment_count'], item['path'],item['type']
            ))

    def drop_table(self, cursor):
        sql = "drop table if EXISTS duanzi"
        cursor.execute(sql)

    def __del__(self):
        pass

# `type`

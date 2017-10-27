# -*- coding: utf-8 -*-
import scrapy
import urlparse
import json
from ..items import DuanziItem
from scrapy_redis.spiders import RedisSpider

#middlewarees 请求和响应
#spider 解析数据
#pipelines 存储数据

class DuanziSpider(scrapy.Spider):
    name = 'duanzi'
    allowed_domains = ['neihanshequ.com']
    start_urls = [
        'http://neihanshequ.com/joke/?is_json=1&app_name=neihanshequ_web',
        'http://neihanshequ.com/pic/?is_json=1&app_name=neihanshequ_web',

    ]
    # redis_key = 'duanzi:start_urls'


    def parse(self, response):
        # navs = response.xpath("//div[@class='site-width']/ul/li[not(contains(@class, 'right'))]")
        # for nav in navs:
        #     duanzi_href = nav.xpath("a/@href").extract_first("")
        #     duanzi_href = urlparse.urljoin(response.url, duanzi_href)
        #     duanzi_text = nav.xpath("a/text()").extract_first("")
        #
        #     yield scrapy.Request(
        #         url=duanzi_href,
        #         callback=self.parse_list,
        #         dont_filter=True,
        #     )
        json_obj = json.loads(response.body)
        if json_obj['message'] == 'success':
            has_more = json_obj['data']['has_more']
            if has_more:
                min_time = json_obj['data']['min_time']
                if "joke" in response.url:
                    url = "http://neihanshequ.com/joke/?is_json=1&app_name=neihanshequ_web&max_time="+str(min_time)
                elif "pic" in response.url:
                    url = "http://neihanshequ.com/pic/?is_json=1&app_name=neihanshequ_web&max_time="+str(min_time)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    dont_filter=True,
                )

        yield scrapy.Request(
                url=response.url,
                callback=self.parse_list,
                dont_filter=True,
            )

    def parse_list(self, response):
        if "joke" in response.url:
            duanzis = json.loads(response.body)['data']['data']
            for duanzi in duanzis:
                text = duanzi['group']['text']
                digg_count = duanzi['group']['digg_count']
                bury_count = duanzi['group']['bury_count']
                repin_count = duanzi['group']['repin_count']
                comment_count = duanzi['group']['comment_count']
                #digg_count 点赞量
                #bury_count 差评
                #repin_count 收藏量
                #comment_count 评论量
                item = DuanziItem()
                item['text'] = text
                item['digg_count'] = digg_count
                item['bury_count'] = bury_count
                item['repin_count'] = repin_count
                item['comment_count'] = comment_count
                item['pic_url_list'] = []
                item['type'] = "joke"
                yield item

        elif "pic" in response.url:
            pics = json.loads(response.body)['data']['data']
            for pic in pics:
                text = pic['group']['text']
                digg_count = pic['group']['digg_count']
                bury_count = pic['group']['bury_count']
                repin_count = pic['group']['repin_count']
                comment_count = pic['group']['comment_count']
                url_list = pic['group']['large_image']['url_list']
                # pic_url_list = []
                # for url in url_list:
                #     pic_url = url['url']
                #     pic_url_list.append(pic_url)
                pic_url_list = [url['url'] for url in url_list]

                item = DuanziItem()
                item['text'] = text
                item['digg_count'] = digg_count
                item['bury_count'] = bury_count
                item['repin_count'] = repin_count
                item['comment_count'] = comment_count

                item['pic_url_list'] = pic_url_list
                item['type'] = "pic"
                yield item

        else:
            print "不是我想要的网址"

    def parse_list_detail(self, response):
        pass

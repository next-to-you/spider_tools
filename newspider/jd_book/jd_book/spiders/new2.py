# -*- coding: utf-8 -*-
import scrapy
from jd_book.items import JdBookItem
from copy import deepcopy
import json
from scrapy_redis.spiders import RedisSpider
# import scrapyd

class New1Spider(RedisSpider):
    name = 'new2'
    allowed_domains = ['jd.com', 'p.3.cn']
    # start_urls = ['https://book.jd.com/booksort.html']

    redis_key = 'book_redis'

    page = 0

    # 爬取导航页， 获取大小分类，并提取连接访问小分类图书列表
    def parse(self, response):
        item = JdBookItem()
        # 提取大分类的列表
        # dt_list = response.xpath('//*[@id="booksort"]/div[2]/dl/dt')
        dt_list = response.xpath('//*[@id="booksort"]/div[2]/dl/dt[1]')  # 取第一个

        for i in dt_list:

            item['big_name'] = i.xpath('.//a/text()').extract_first()
            # small_list = i.xpath('./following-sibling::*[1]/em')
            small_list = i.xpath('./following-sibling::*[1]/em[1]')  # 取第一个

            for small_name in small_list:
                item['small_name'] = small_name.xpath('./a/text()').extract_first()
                url = 'https:' + small_name.xpath('./a/@href').extract_first()

                # 发送小分页请求，并传递给目标页的解析函数
                yield scrapy.Request(url, callback=self.parse_book_list, meta={'item': deepcopy(item)})

    # 爬取小分类列表的图书信息
    def parse_book_list(self, response):
        item1 = response.meta['item']

        book_list = response.xpath('//*[@id="plist"]/ul/li')

        for i in book_list:
            item1['name'] = i.xpath('.//div[@class="p-name"]//em/text()').extract_first().strip()

            item1['img_link'] = 'https:' + str(i.xpath('.//a/img/@src').extract_first() or i.xpath('.//a/img/@data-lazy-img').extract_first())

            # item['price'] = response.xpath('.//div[@class="p-name"]//em/text()').extract_first()
            item1['publisher'] = i.xpath('.//span[1]/span/a/text()').extract_first().strip()
            item1['author'] = i.xpath('.//span[@class="author_type_1"]/a/text()').extract()
            item1['publish_time'] = i.xpath('.//span[@class="p-bi-store"]/a/@title').extract_first()

            url = 'https://p.3.cn/prices/mgets?skuIds=J_' + response.xpath('//div/@data-sku').extract_first()

            # print(item1)
            yield response.follow(url, callback=self.parse_price, meta={'item': deepcopy(item1)})

        # 翻页获取
        self.page += 1
        if not response.xpath('//a[@class="pn-next"]/@href'):
            return

        if self.page > 4:
            return

        next_url = 'https://list.jd.com' + response.xpath('//a[@class="pn-next"]/@href').extract_first()
        # yield scrapy.Request(next_url, callback=self.parse_book_list, meta={'item': item1})
        yield response.follow(next_url, callback=self.parse_book_list, meta={'item': item1})

    # 请求图书价格
    def parse_price(self, response):
        item = response.meta['item']

        a = response.body.decode()
        item['price'] = (json.loads(a))[0]['p']
        # print(item)

        yield item



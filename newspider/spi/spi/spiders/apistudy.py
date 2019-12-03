# -*- coding: utf-8 -*-
import scrapy
from spi.items import SpiItem

"""
1.采用scrapy框架爬去pm2.5数据, 此段只爬取部分数据,需要修改选择器来完善爬去数据
2. 未采用crawl爬取,未采用scrapy_redis
3. 未采用scrapy的下载器爬取数据,使用selenium爬取数据
4. 管道保存采用json管道,csv管道,mongodb管道,redis存储,后续其他爬虫可以借鉴完善
"""
class ApistudySpider(scrapy.Spider):
    name = "apistudy"
    allowed_domains = ["aqistudy.cn"]
    start_urls = (
        'https://www.aqistudy.cn/historydata/',
    )

    def parse(self, response):
        item = SpiItem()
        # city_list = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div[2]/li/a')
        city_list = response.xpath('/html/body/div[3]/div/div[1]/div[2]/div[2]/ul[1]/div[2]/li[1]/a')
        for i in city_list:
            item['city'] = i.xpath('.//text()').extract_first()
            url = self.start_urls[0] + i.xpath('./@href').extract_first()
            yield scrapy.Request(url, callback=self.parse_month, meta={'api': item})

    # 月份解析
    def parse_month(self, response):
        # print(response.body().decode())
        # print('$$' * 50,response)
        item = response.meta['api']
        month_list = response.xpath('//tr[3]/td/a')
        print(month_list)
        for i in month_list:
            # url = i.xpath('./@href')
            # print(url)
            url = self.start_urls[0] + i.xpath('./@href').extract_first()
            print(url)

            yield scrapy.Request(url, callback=self.parse_day, meta={'api': item})
        # item['month'] = response.xpath('/html/body/div[3]/div[1]/div[1]/table/tr/td[1]/a')


    def parse_day(self, response):
        # print('*$*$' * 50)
        item = response.meta['api']
        day_list = response.xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr')
        # 去掉列表的表头
        day_list.pop(0)

        for i in day_list:
            item['day'] = i.xpath('./td[1]//text()').extract_first()
            item['aqi'] = i.xpath('./td[2]//text()').extract_first()
            item['level'] = i.xpath('./td[3]//text()').extract_first()
            item['pm2_5'] = i.xpath('./td[4]//text()').extract_first()
            item['pm10'] = i.xpath('./td[5]//text()').extract_first()
            item['so_2'] = i.xpath('./td[6]//text()').extract_first()
            item['co'] = i.xpath('./td[7]//text()').extract_first()
            item['no_2'] = i.xpath('./td[8]//text()').extract_first()
            item['o3_8h'] = i.xpath('./td[9]//text()').extract_first()

            yield item
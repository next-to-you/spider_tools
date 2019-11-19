from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from spi.items import SpiItem


class AqiSpider(CrawlSpider):
    name = 'aqi_spider'
    allowed_domains = ['aqistudy.cn']

    # 起始url
    start_urls = ['https://www.aqistudy.cn/historydata/',]

    # 默认 没有callback   follow = True
    # 默认 有callback   follow = false

    rules = (
        # 提取城市的链接
        # LinkExtractor参数 allow为允许的url匹配
        # Rule(LinkExtractor(restrict_xpaths='/html/body/div[3]/div/div[1]/div[2]/div[2]/ul/div[2]'), follow=True),
        Rule(LinkExtractor(allow=r'monthdata', restrict_xpaths='/html/body/div[3]/div/div[1]/div[2]/div[2]/ul[2]/div[2]/li[1]'), follow=True),

        # 提取所有月份的链接
        # Rule(LinkExtractor(restrict_xpaths='/html/body/div[3]/div[1]/div[1]/table/tbody/tr/td[1]'), follow=True, ),
        Rule(LinkExtractor(restrict_xpaths='/html/body/div[3]/div[1]/div[1]/table/tbody/tr[2]/td[1]'), callback='parse_day', follow=True, ),

        # 提取所有日期份数据,并交给解析函数
        # Rule(follow=False, callback='parse_day'),
    )

    # 解析数据

    def parse_day(self, response):
        # print('*$*$' * 50)
        item = SpiItem()
        day_list = response.xpath('/html/body/div[3]/div[1]/div[1]/table/tbody/tr')
        # 去掉列表的表头
        day_list.pop(0)
        item['city'] = response.xpath('//*[@id="title"]/text()').extract_first()[8:-11]

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

from copy import deepcopy
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from jd_book.items import JdBookItem
from scrapy_redis.spiders import RedisCrawlSpider

# import scrapyd

class AqiSpider(RedisCrawlSpider):
    name = 'jd_spider'
    allowed_domains = ['jd.com', 'p.3.cn']

    redis_key = "jd_book:start_url"

    # 起始url
    # start_urls = ['https://book.jd.com/booksort.html']

    # 默认 没有callback   follow = True
    # 默认 有callback   follow = false

    rules = (
        # 提取所有的二级分类链接,  一级分类没有所有未爬取
        # Rule(LinkExtractor(restrict_xpaths='//*[@id="booksort"]/div[2]/dl/dd/em'), follow=True, ),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="booksort"]/div[2]/dl/dd[25]/em[1]/a'), follow=True, ),

        # 提取商品列表页中所有的商品详情页链接
        Rule(LinkExtractor(restrict_xpaths='//*[@id="plist"]/ul/li//div[@class="p-img"]'), callback='parse_goods', follow=True),

        # 翻页爬取
        # Rule(LinkExtractor(restrict_xpaths='//*[@id="J_bottomPage"]/span[1]'), follow=True, ),

        # 详情页爬取
        # Rule(LinkExtractor(restrict_xpaths='//*[@id="choose-attr-1"]/div[2]//div/a'), callback='parse_goods', follow=True),
    )

    # 解析数据
    def parse_goods(self, response):
        item1 = JdBookItem()

        # 一级分类
        item1['class_1_name'] = response.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[1]/a/text()').extract_first().strip()
        # 二级分类
        item1['class_2_name'] = response.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[3]/a/text()').extract_first().strip()
        # 三级分类
        item1['class_3_name'] = response.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[5]/a/text()').extract_first().strip()
        # 有些图书没有四级分类,这里判断一下
        # 四级分类
        item1['class_4_name'] = response.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[7]/a/text()').extract_first()
        if item1['class_4_name']:
            item1['class_4_name'].strip()

        # 书名
        item1['name'] = response.xpath('//*[@id="crumb-wrap"]/div/div[1]/div[@class="item ellipsis"]/@title').extract_first()

        # 图书链接
        item1['img_link'] = list(map(self.image_link, response.xpath('//*[@id="spec-list"]/div/ul/li/img/@src').extract()))

        # item['price'] = response.xpath('.//div[@class="p-name"]//em/text()').extract_first()
        # 出版社, 由于需要条件过滤,暂时不考虑此项
        # item1['publisher'] = response.xpath('//*[@id="parameter2"]/li[1]/a/@title').extract_first().strip()
        # 商品id,获取商品价格
        sku_id = response.xpath('//a[@id="choose-btn-coll"]/@data-id').extract_first().strip()
        # 作者
        item1['author'] = response.xpath('//*[@id="p-author"]/a[1]/text()').extract()

        url = 'https://p.3.cn/prices/mgets?skuIds=J_' + sku_id

        # print(item1)
        # item = deepcopy(item1)
        yield response.follow(url, callback=self.parse_price, meta={'item': item1})

    def image_link(self, link):
        link = 'https:' + link
        return link

    # 请求图书价格
    def parse_price(self, response):
        item = response.meta['item']

        a = response.body.decode()
        item['price'] = (json.loads(a))[0]['p']
        # print(item)

        yield item


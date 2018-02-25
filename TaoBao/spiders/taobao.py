# -*- coding: utf-8 -*-
import scrapy
import re
from ..settings import QUESTION, COOKIES, WAIT_TIME
from ..items import TaobaoItem
from urllib.parse import urljoin
from scrapy_splash import SplashRequest


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['taobao.com']
    start_urls = ['https://s.taobao.com/search?q={q}'.format(q=QUESTION)]

    """可以通过script脚本设置不加载图片"""
    # script = """
    # function main(splash)
    #     splash.images_enabled = false
    #     return splash:html()
    # """

    """设置images为0不加载图片，默认为1加载图片"""
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url, callback=self.parse, endpoint='render.html', args={'wait': WAIT_TIME, 'cookies': COOKIES, 'images': 0}
            )

    """解析商品列表页信息"""
    def parse(self, response):
        goods = response.css('div.item.J_MouserOnverReq')
        for good in goods:
            title = good.css('div.row.row-2.title a.J_ClickStat::text').extract()
            if isinstance(title, list):
                title = ''.join(title).strip()
            price = good.css('div.price.g_price.g_price-highlight strong::text').extract_first()
            free_shipping = 'Yes' if good.css('div.ship.icon-service-free') else 'No'
            month_sale = good.css('div.deal-cnt::text').extract_first()
            month_sale = re.match(r'\d+', month_sale).group(0)
            goods_url = good.css('div.row.row-2.title a.J_ClickStat::attr(href)').extract_first()

            shop = good.xpath('//div[@class="shop"]/a/span[2]/text()').extract_first()
            shop_type = '天猫' if good.css('span.icon-service-tianmao') else '淘宝'
            addr = good.css('div.location::text').extract_first()
            data = {
                'title': title,
                'price': price,
                'free_shipping': free_shipping,
                'month_sale' : month_sale,
                'goods_url': goods_url,
                'shop': shop,
                'shop_type': shop_type,
                'addr': addr
            }
            """使用scrapy.Request需要设置html=1, 如果不加载图片还要设置images=0"""
            # yield scrapy.Request(urljoin('https:', goods_url), callback=self.parse_grade, meta={
            #     'data': data,
            #     'endpoint': 'render.html',
            #     'splash': {'args': {'html': 1, 'wait': WAIT_TIME, 'cookies': COOKIES}}
            # })
            yield SplashRequest(urljoin('https:', goods_url), callback=self.parse_grade, endpoint='render.html', meta={'data': data}, args={
                'wait': WAIT_TIME,
                'cookies': COOKIES,
                'images': 0
            })

        """ 获取下一页链接"""
        try:
            next_key = response.css('li.next a::attr(data-key)').extract_first()
            next_value = response.css('li.next a::attr(data-value)').extract_first()
            next_url = self.start_urls[0] + '&' + next_key + '=' + next_value
            self.logger.debug('tring to crawl newpage .............')
            yield SplashRequest(
                next_url, callback=self.parse, endpoint='render.html', args={'wait': WAIT_TIME, 'cookies': COOKIES, 'images': 0}
                                )
        except:
            self.logger.info('all pages have been crawled')

    """解析商品详情页信息"""
    def parse_grade(self, response):
        item = TaobaoItem()
        data = response.meta['data']
        item['title'] = data['title']
        item['price'] = data['price']
        item['free_shipping'] = data['free_shipping']
        item['month_sale'] = data['month_sale']
        item['goods_url'] = data['goods_url']
        item['shop'] = data['shop']
        item['shop_type'] = data['shop_type']
        item['addr'] = data['addr']

        """淘宝页面格式较多，这里取其中常见的两种"""
        if item['shop_type'] == '天猫':
            same_grade = response.css('div.shopdsr-score.shopdsr-score-up-ctrl span::text').extract()
            if not same_grade:
                same_grade = response.css('#shop-info div.main-info span::text').extract()
        else:
            same_grade = response.css('div.tb-shop-rate a::text').extract()
            if not same_grade:
                same_grade = response.css('ul.shop-service-info-list em::text').extract()
        if len(same_grade) == 3:
            item['same_grade'] = float(same_grade[0].strip())
            item['service_grade'] = float(same_grade[1].strip())
            item['shipping_grade'] = float(same_grade[2].strip())

        if len(item.keys()) != 11:
            for field in item.fields:
                if field not in item.keys():
                    item[field] = None

        yield item


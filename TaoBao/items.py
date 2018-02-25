# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    free_shipping = scrapy.Field()
    month_sale = scrapy.Field()
    goods_url = scrapy.Field()
    shop = scrapy.Field()
    shop_type = scrapy.Field()
    addr = scrapy.Field()
    same_grade = scrapy.Field()
    service_grade = scrapy.Field()
    shipping_grade = scrapy.Field()

    def get_sql(self):
        sql = """
        INSERT INTO info
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE goods_url=VALUES(goods_url)
        """
        values = (self['title'], self['price'], self['free_shipping'], self['month_sale'], self['goods_url'], self['shop'],
                  self['shop_type'], self['addr'], self['same_grade'], self['service_grade'], self['shipping_grade'])
        return sql.strip(), values






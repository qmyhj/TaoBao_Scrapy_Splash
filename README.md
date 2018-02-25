# TaoBao_Scrapy_Splash
基于Scrapy-Splash爬取淘宝商品信息并存储到mysql中

1 由于淘宝商品页面格式多样，本爬虫适用于其中的大部分，对于部分商品可能不适应，爬取的关键词需到settings文件中配置QUESTION参数

2 本爬虫基于Scrapy-Splash爬取了淘宝商品列表页和详情页，并提供了mysql存储接口，需要到settings文件中配置MYSQL_PARAMS参数

3 由于爬取天猫详情页时需要Cookie，运行爬虫前需要到settings文件中配置淘宝Cookie参数

4 运行爬虫，需要先运行$ docker run -p 8050:8050 scrapinghub/splash，然后运行main.py即可

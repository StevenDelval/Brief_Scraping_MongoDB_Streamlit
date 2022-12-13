import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ImdbItem


class ImdbCrawlSpiderSpider(CrawlSpider):
    name = 'imdb_crawl_spider'
    allowed_domains = ['imdb.com']

    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0'

    link_imdb_details = LinkExtractor(restrict_xpaths="//td[@class='titleColumn']/a")
    
    rule_imdb_details= Rule(link_imdb_details, callback='parse_item', follow=True)
    
    rules = (
        rule_imdb_details,
    )
    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/chart/top/', headers={
            'User-Agent': self.user_agent
        })


    def parse_item(self, response):
        item = ImdbItem()
        item["titre"] = response.xpath("//h1/text()").extract()
        item["titre_original"] = response.xpath("//div[@class='sc-dae4a1bc-0 gwBsXc']/text()").extract()
        item["score"] = response.xpath("//span[@class='sc-7ab21ed2-1 jGRxWM']/text()").extract_first()
        item["genre"] = response.xpath("//a[@class='sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt']/span/text()").extract()
        item["date"] = response.css("div.sc-80d4314-2 > ul >li:first-child>a::text").extract()
        item["duree"] = response.css("div.sc-80d4314-2 > ul >li:last-child::text").extract()
        item["descriptions"] = response.xpath("/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/p/span[3]/text()").extract()
        item["acteurs"] = response.xpath("/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[3]/div/ul/li/a/text()").extract()
        item["public"] = response.xpath("/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[2]/a/text()").extract()
        item["pays"] = response.xpath("/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[@class='ipc-page-section ipc-page-section--base celwidget']/div[@class='sc-f65f65be-0 ktSkVi']/ul[@class='ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base']/li[@class='ipc-metadata-list__item'][1]/div[@class='ipc-metadata-list-item__content-container']/ul[@class='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base']/li[@class='ipc-inline-list__item']/a[@class='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link']/text()").extract()
        
        
        yield item

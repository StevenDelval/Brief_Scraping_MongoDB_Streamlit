import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ImdbItem
from .functions import convertion_duree

class ImdbCrawlSpiderSpider(CrawlSpider):
    name = 'imdb_crawl_spider'
    custom_settings = {
        'ITEM_PIPELINES': {
            'imdb.pipelines.ImdbPipeline': 400
        }
    }

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
        item["titre"] = ''.join(response.xpath("//h1/text()").extract())
        item["titre_original"] = ''.join(response.xpath("//div[@class='sc-dae4a1bc-0 gwBsXc']/text()").extract()).replace("Original title: ",'')
        item["score"] = round(float(response.xpath("//span[@class='sc-7ab21ed2-1 jGRxWM']/text()").extract_first()),2)
        item["genre"] = response.xpath("//a[@class='sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt']/span/text()").extract()
        item["date"] = int(''.join(response.css("div.sc-80d4314-2 > ul >li:first-child>a::text").extract()))
        item["duree"] = convertion_duree(''.join(response.css("div.sc-80d4314-2 > ul >li:last-child::text").extract()).replace(",",''))
        item["descriptions"] = ''.join(response.xpath("//div/div/p/span[@class='sc-16ede01-2 gXUyNh']/text()").extract())

        if item["descriptions"] =="":
            item["descriptions"] = ''.join(response.xpath("//div[@data-testid='plot']/span[@data-testid='plot-xl']/text()").extract())

        item["acteurs"] = response.xpath("/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li[3]/div/ul/li/a/text()").extract()
        item["public"] = ''.join(response.xpath("/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[2]/a/text()").extract())
        item["pays"] = response.xpath("//section/div/ul/li[@class = 'ipc-metadata-list__item'][1]/div[@class = 'ipc-metadata-list-item__content-container']/ul/li/a[@class = 'ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link']/text()").extract()
        item["url"] = ''.join(response.xpath("/html/body/div[2]/main/div/section[1]/section/div/section/section/div/div/div/div[1]/div/div/img/@src").extract())
        if ["url"] == "":
            item["url"] = ''.join(response.xpath("//div[@data-cel-widget='DynamicFeature_HeroPoster']/div/img/@src").extract())

        item["langue"]= response.xpath("//section[@data-testid='Details']/div[@data-testid='title-details-section']/ul/li[@data-testid='title-details-languages']/div/ul/li/a/text()").extract()

        yield item

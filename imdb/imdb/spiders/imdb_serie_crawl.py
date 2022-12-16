import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ImdbItem,ImdbSerieItem
from .functions import convertion_duree

class ImdbCrawlSpiderSpider(CrawlSpider):
    name = 'imdb_serie_crawl'
    custom_settings = {
        'ITEM_PIPELINES': {
            'imdb.pipelines.ImdbSeriePipeline': 400
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
        yield scrapy.Request(url='https://www.imdb.com/chart/toptv/', headers={
            'User-Agent': self.user_agent
        })


    def parse_item(self, response):
        item = ImdbSerieItem()
        item["titre"] = ''.join(response.xpath("//h1/text()").extract())
        item["titre_original"] = ''.join(response.xpath("//div[@class='sc-dae4a1bc-0 gwBsXc']/text()").extract()).replace("Original title: ",'')
        item["score"] = round(float(response.xpath("//span[@class='sc-7ab21ed2-1 jGRxWM']/text()").extract_first()))
        item["genre"] = response.xpath("//a[@class='sc-16ede01-3 bYNgQ ipc-chip ipc-chip--on-baseAlt']/span/text()").extract()
        item["duree"] = convertion_duree(''.join(response.css("div.sc-80d4314-2 > ul >li:last-child::text").extract()).replace(",",''))
        item["date"] = ''.join(response.xpath("//ul[@data-testid='hero-title-block__metadata']/li[2]/a/text()").extract())
        
        item["descriptions"] = ''.join(response.xpath("/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/p/span[3]/text()").extract())
        item["acteurs"] = response.xpath("/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[3]/ul/li/div/ul/li/a/text()").extract()
        item["public"] = ''.join(response.xpath("/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div/ul/li[3]/a/text()").extract())
        item["pays"] = response.xpath("/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[@class='ipc-page-section ipc-page-section--base celwidget']/div[@class='sc-f65f65be-0 ktSkVi']/ul[@class='ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base']/li[@class='ipc-metadata-list__item'][1]/div[@class='ipc-metadata-list-item__content-container']/ul[@class='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content base']/li[@class='ipc-inline-list__item']/a[@class='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link']/text()").extract()
        item["episode"] = int(''.join(response.xpath("//section[@data-testid='DynamicFeature_Episodes']/div[@data-testid='episodes-header']/a/h3/span[2]/text()").extract()))
        item["nb_saison"]=''.join(response.xpath("//section[@data-testid='DynamicFeature_Episodes']/div/div[@data-testid='episodes-browse-episodes']/div/a[2]/div/text()").extract())
        if item["nb_saison"] =="":
            item["nb_saison"]=''.join(response.xpath("//section[@data-testid='DynamicFeature_Episodes']/div/div[@data-testid='episodes-browse-episodes']/div/div[1]/label/text()").extract())
        yield item

        
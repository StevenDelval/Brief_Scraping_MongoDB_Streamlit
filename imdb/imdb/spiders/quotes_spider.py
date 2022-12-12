import scrapy
from ..items import ImdbItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://quotes.toscrape.com/',
    ]

    def parse(self, response):
        items = ImdbItem()
        all_div_quotes = response.css("div.quote")
        
        for quote_div in all_div_quotes:

            quote = quote_div.css("span.text::text").extract()
            author = quote_div.css(".author::text").extract()


            items['quote'] = quote
            items['author'] = author

            yield items


import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://quotes.toscrape.com/',
    ]

    def parse(self, response):
        all_div_quotes = response.css("div.quote")
        quotes = all_div_quotes.css("span.text::text").extract()
        authors = all_div_quotes.css(".author::text").extract()
        for div_quote in all_div_quotes:
            quote = div_quote.css("span.text::text").extract()
            author = div_quote.css(".author::text").extract()
            yield {
            "quote" : quote,
            "author" : author,
            }

        
        yield {
            "quotes" : quotes,
            "authors" : authors,
            }


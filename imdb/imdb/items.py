# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
   
    titre_original = scrapy.Field()
    score = scrapy.Field()
    descriptions = scrapy.Field()
    acteurs = scrapy.Field()
    public = scrapy.Field()
    duree = scrapy.Field()
    pays = scrapy.Field()
    date = scrapy.Field()
    genre = scrapy.Field()
    titre = scrapy.Field()
    url = scrapy.Field()
    langue = scrapy.Field()

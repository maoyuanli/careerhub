import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
import re


def preClean(raw):
    decoded =  re.sub(r'[^\x00-\x7F]+',' ', raw)
    for unwanted in [r'\\n',r'"']:
        if unwanted in decoded:
            return decoded.replace(unwanted,' ')
        else:
            return decoded
# def removePunc(raw):
#     return raw.replace('"','').replace(r'\n','').replace(u"\u2013",'')


class JobItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(str.strip, preClean),
        output_processor=TakeFirst()
    )
    company = scrapy.Field(
        input_processor=MapCompose(str.strip, preClean),
        output_processor=TakeFirst()
    )
    descr = scrapy.Field(
        input_processor=MapCompose(str.strip, preClean),
        output_processor=TakeFirst()
    )
    link = scrapy.Field(
        output_processor=TakeFirst()
    )

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
import re


def pre_clean(raw):
    decoded = re.sub(r'[^\x00-\x7F]+', ' ', raw)
    for unwanted in [r'\\n', r'"']:
        if unwanted in decoded:
            return decoded.replace(unwanted, ' ')
        else:
            return decoded


class JobItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(str.strip, pre_clean),
        output_processor=TakeFirst()
    )
    company = scrapy.Field(
        input_processor=MapCompose(str.strip, pre_clean),
        output_processor=TakeFirst()
    )
    descr = scrapy.Field(
        input_processor=MapCompose(str.strip, pre_clean),
        output_processor=TakeFirst()
    )
    link = scrapy.Field(
        output_processor=TakeFirst()
    )

import re

import scrapy
import w3lib.html as w3htlm
from scrapy.loader.processors import MapCompose, TakeFirst


def pre_clean(raw):
    decoded = re.sub(r'[^\x00-\x7F]+', ' ', raw)
    decoded = decoded.replace(r'"', ' ')
    decoded = w3htlm.replace_escape_chars(decoded)
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

import scrapy
from scrapy.loader import ItemLoader
from indeed.items import JobItem


class Jobs(scrapy.Spider):
    name = 'jobs'

    def __init__(self, keywords='', *args, **kwargs):
        super(Jobs, self).__init__(*args, **kwargs)
        self.start_urls = self.link_builder(keywords)

    def __str__(self):
        return 'indeed jobs spider'

    def link_builder(self, param_string: str):
        keyWords = param_string.split(' ')
        keyWords = [kw.strip() for kw in keyWords]
        prefix = 'https://ca.indeed.com/jobs?q='
        ending = '&l=Toronto%2C+ON'
        middle = '+'.join(keyWords)
        return prefix + middle + ending

    def start_requests(self):
        urls = [
            self.start_urls
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list_page)

    def parse_list_page(self, response):
        for title in response.xpath("""//div[@class='title']"""):
            detail_url = 'http://indeed.ca' + title.xpath(""".//a/@href""").extract_first()
            yield scrapy.Request(url=detail_url, callback=self.parse_detail_page)

        next_page_selector = r"""//span[@class='np' and contains(text(),'Next')]/../../@href"""
        next_page = response.xpath(next_page_selector).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page), callback=self.parse_list_page
            )

    def parse_detail_page(self, response):
        layouts = response.xpath(
            """//div[@class='jobsearch-ViewJobLayout-jobDisplay icl-Grid-col icl-u-xs-span12 icl-u-lg-span7']""")
        for layout in layouts:
            loader = ItemLoader(item=JobItem(), selector=layout, response=response)
            loader.add_xpath('title', r"""//h3/text()""")
            loader.add_xpath('company', r"""//div[@class="icl-u-lg-mr--sm icl-u-xs-mr--xs"]/text()""")
            loader.add_xpath('descr', r"""string(//div[@id='jobDescriptionText']/div)""")
            loader.add_value('link', response.url)
            yield loader.load_item()

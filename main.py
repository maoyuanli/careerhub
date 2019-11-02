import os
import sys

from scrapy.cmdline import execute

from utils.popup import Popup
from utils.jd_etl import JobDescriptionETL


class JobDescriptionDistiller:
    def __init__(self, source, output):
        self.source = source
        self.output = output

    def crawl(self):
        pop = Popup()
        pop_input = pop.keywords_input()

        if pop_input is not None:
            keywords = pop_input.strip()
        else:
            keywords = ''

        if keywords != '':
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            try:
                os.remove(self.source)
            finally:
                execute(['scrapy', 'crawl', 'jobs', '-a', 'keywords={0}'.format(keywords), '-o', self.source])
        else:
            pop.msgbox('No Keyword Entered', 'Please enter the keyword(s)')

    def distill(self):
        jobetl = JobDescriptionETL(self.source, self.output)
        jobetl.etl()


if __name__ == '__main__':
    jdd = JobDescriptionDistiller(r'resources/crawled_jd.json', r'resources/distilled_jd.json')
    jdd.crawl()
    jdd.distill()


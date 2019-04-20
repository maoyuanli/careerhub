from scrapy.cmdline import execute
import os
import sys
from Popup import Popup

pop = Popup()
inputFromPop = pop.keywordsInput()

if inputFromPop is not None:
    keywords = inputFromPop.strip()
else:
    keywords = ''

if keywords != '':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        os.remove('data.json')
    finally:
        execute(["scrapy","crawl","jobs","-a","keywords={0}".format(keywords),"-o","data.json"])
else:
    pop.msgbox('No Keyword Entered', 'Please enter the keyword(s)')
from utils.crawl_etl import JobDescriptionCrawler

if __name__ == '__main__':
    raw_output = r'resources/crawled_jd.json'
    crawler = JobDescriptionCrawler(raw_output)
    crawler.crawl()

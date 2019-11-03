from utils.crawl_etl import JobDescriptionCrawler

if __name__ == '__main__':
    raw_data = r'resources/crawled_jd.json'
    clean_data = r'resources/distilled_jd.json'
    crawler = JobDescriptionCrawler(raw_data, clean_data)
    crawler.crawl()

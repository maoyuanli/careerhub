from utils.crawl_etl import JobDescriptionETL

if __name__ == '__main__':
    raw_data = r'resources/crawled_jd.json'
    clean_data = r'resources/distilled_jd.json'
    jdetl = JobDescriptionETL(raw_data, clean_data)
    jdetl.etl()
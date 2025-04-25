import scrapy


class DivanScrapeSpider2Spider(scrapy.Spider):
    name = "divan_scrape_spider2"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    def parse(self, response):
        pass

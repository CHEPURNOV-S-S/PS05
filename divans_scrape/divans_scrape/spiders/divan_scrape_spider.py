#/spiders/divan_scrape_spider
import scrapy


class DivanScrapeSpider(scrapy.Spider):
    name = "divan_scrape_spider"
    allowed_domains = ["https://www.divan.ru/"]
    start_urls = ["https://www.divan.ru/category/svet"]

    def parse(self, response):
        lights = response.css('div.WdR1o')
        for light in lights:
            yield {
            # Ссылки и теги получаем с помощью консоли на сайте
            # Создаём словарик названий, используем поиск по диву, а внутри дива — по тегу span
            'name' : light.css('div.lsooF span::text').get(),
            # Создаём словарик цен, используем поиск по диву, а внутри дива — по тегу span
            'price' : light.css('div.pY3d2 span::text').get(),
            # Создаём словарик ссылок, используем поиск по тегу "a", а внутри тега — по атрибуту
            # Атрибуты — это настройки тегов
            'url' : light.css('a').attrib['href']
            }
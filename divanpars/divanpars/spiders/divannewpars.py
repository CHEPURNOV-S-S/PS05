import scrapy


class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/divany-i-kresla"]


    def parse(self, response, **kwargs):

        # with open("page_dump.html", "w", encoding="utf-8") as file:
        #     file.write(response.text)
        #     self.logger.info("HTML-код страницы сохранён в page_dump.html")
        self.logger.info(f"parse start{response.url}")
        divans = response.css('div._Ud0k')
        # Настраиваем работу с каждым отдельным диваном в списке
        for divan in divans:
            yield {
                'name' : divan.css('div.lsooF span::text').get(),
                'price' : divan.css('div.pY3d2 span::text').get(),
                'url' : divan.css('a').attrib['href']
            }
        self.logger.info("parse end")
        # Попытка найти кнопку "Следующая страница" и выполнить клик
        try:
            self.logger.info("Поиск следующей страницы")
            next_page_link = response.css('a[data-testid="item"] svg[data-testid="arrow-right"]').xpath(
                "../@href").get()
            if next_page_link:
                self.logger.info(f"Найдена подходящая ссылка: {next_page_link}")
                yield response.follow(next_page_link, callback=self.parse)
            else:
                raise ValueError("No more pages to crawl")
        except Exception as e:
            self.logger.info("No more pages to crawl or error occurred: %s", e)



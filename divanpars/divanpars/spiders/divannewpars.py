import random
from contextlib import nullcontext

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import time


class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/divany-i-kresla"]

    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)

       # Настройка Selenium WebDriver
       chrome_options = Options()
       chrome_options.add_argument("start-maximized")
       chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
       chrome_options.add_experimental_option('useAutomationExtension', False)
       chrome_options.add_argument("--disable-blink-features=AutomationControlled")
       #chrome_options.add_argument('--headless')  # Безголовый режим
       #service = Service('C:\Program Files\Google\Chrome\chromedriver_win32\chromedriver.exe')
       chrome_options.add_argument(
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36")
       self.driver = webdriver.Chrome(options=chrome_options)
       # Настройка Selenium Stealth
       stealth(self.driver,
               languages=["en-US", "en"],
               vendor="Google Inc.",
               platform="Win32",
               webgl_vendor="Intel Inc.",
               renderer="Intel Iris OpenGL Engine",
               fix_hairline=True,
               )
       # Тестирование
       self.driver.get("https://bot.sannysoft.com/")
       time.sleep(5)  # Ожидание загрузки страницы
       self.driver.save_screenshot("selenium_test.png")  # Сохранение скриншота


    def parse(self, response, **kwargs):

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
            self.logger.info(f"selenium get url: {response.url}")
            # Используем Selenium для загрузки страницы
            self.driver.get(response.url)
            time.sleep(30)  # Ожидание загрузки страницы
            # html_content = self.driver.page_source
            # with open(f"html_content.html", "w", encoding="utf-8") as file:
            #     file.write(html_content)
            self.logger.info("Поиск следующей страницы")

            pagination_links = self.driver.find_elements(By.CSS_SELECTOR, "a.ui-GPFV8.ui-BjeX1.ui-gI0j8.PaginationLink")
            href_value = None
            # Вывод ссылок
            for link in pagination_links:
                svg_elements = link.find_elements(By.XPATH, ".//*[local-name()='svg' and @data-testid='arrow-right']")
                if svg_elements:
                    href_value = link.get_attribute("href")
                    self.logger.info(f"Найдена подходящая ссылка: {href_value}")
                    break  # Если нужна только первая подходящая ссылка

            if href_value:
                yield response.follow(href_value, callback=self.parse, dont_filter=True)
                #yield Request(url=href_value, callback=self.parse)
            else:
                raise ValueError("No more pages to crawl")
        except Exception as e:
            self.logger.info("No more pages to crawl or error occurred: %s", e)

    def closed(self, reason):
       # Закрытие Selenium WebDriver при завершении работы паука
       self.driver.quit()


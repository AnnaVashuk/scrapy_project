import scrapy
import csv

class CatsSpider(scrapy.Spider):
    name = "cats"
    allowed_domains = ["ru.wikipedia.org"]
    start_urls = ["https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D0%BF%D0%BE%D1%80%D0%BE%D0%B4_%D0%BA%D0%BE%D1%88%D0%B5%D0%BA"]

    def parse(self, response):
        breed_links = response.css('tbody tr td:nth-child(2) a::attr(href)').getall()

        for breed_link in breed_links:
            yield response.follow(breed_link, callback=self.parse_pep_data)

    def parse_pep_data(self, response):
        breed_info = {
            'name': response.css('h1.firstHeading span::text').get(),
            'country': response.css('table.infobox tbody tr:contains("Страна") td:nth-child(2) a::text').get().strip() if response.css('table.infobox tbody tr:contains("Страна") td:nth-child(2) a::text').get() else None,
            'year': response.css('table.infobox tbody tr:contains("Год") td a::text').get(),
            'category': response.css('table.infobox tbody tr:contains("Категория") td::text').get(),
            'standard': response.css('table.infobox tbody tr:contains("Стандарт") td a::text').get(),
        }
        self.save_to_csv(breed_info)

        yield breed_info

    def save_to_csv(self, breed_info):
        with open('breed_info.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=breed_info.keys())

            if file.tell() == 0:
                writer.writeheader()

            writer.writerow(breed_info)

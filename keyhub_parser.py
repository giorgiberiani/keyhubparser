import scrapy
import os
class KeyhubParser(scrapy.Spider):

    name = 'keyhub'

    start_urls = [
        'https://www.keyhub.com/en/'
    ]

    url = 'https://www.keyhub.com/en/category/{}/'

    allowed_domains = [
        'keyhub.com'
    ]

    categories = ['pc', 'console', 'carte-points-cadeau-abonnement']

    def parse(self, response):
        for category in self.categories:
            url = self.url.format(category)

            yield scrapy.Request(url, self.get_pages)


    def parse_pages(self, response):
        number_of_pages = response.xpath('//*[@title="Last Page"]/@href').extract_first()
        number_of_pages = int(number_of_pages.split('=')[-1]) + 1

        for page in range(1,number_of_pages):
            url = response.url+'?page={}'.format(page)
            yield scrapy.Request(url, self.get_game_urls)

    def parse_game_urls(self, response):
        urls = response.xpath('//*[@class="category_bottom"]/div[@class="category_title"]/h3/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, self.parse_content)

    def parse_images(self, response):

        image_url = response.xpath('//*[@itemprop="image"]/@src').extract_first()
        # game_name = response.xpath('//*[@class="title"]/text()').extract_first()
        image_name = image_url.split('/')[-1]
        image_local_path = '/home/beriani/data/keyhub/{}'.format(image_name)
        os.system('curl {} > {}'.format(image_url, image_local_path))

 


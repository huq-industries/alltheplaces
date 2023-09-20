import base64
import json
import scrapy
from locations.items import Feature

class RalphLaurenSpider(scrapy.Spider):
    name = 'ralph_lauren'
    allowed_domains = ['www.ralphlauren.com']
    start_urls = ('https://www.ralphlauren.com/Stores-ShowCountries',)

    def parse(self, response):
        countries = response.xpath('//a[@class="store-directory-countrylink"]/@href').extract()
        for country in countries:
            url = '/findstores?dwfrm_storelocator_country=' + country.split('=', 1)[1] + '&dwfrm_storelocator_findbycountry=Search&findByValue=CountrySearch'
            yield scrapy.Request(response.urljoin(url), callback=self.parse_city)

    def parse_city(self, response):
        stores = response.xpath('//span[@class="store-listing-name"]/a/@href').extract()
        for store in stores:
            yield scrapy.Request(response.urljoin(store), callback=self.parse_locations)

    def parse_locations(self, response):
        data = response.xpath('//div[@class="storeJSON hide"]/@data-storejson').extract_first()
        hours = response.xpath('//tr[@class="store-hourrow"]//td//text()').getall()
        opening_hours = []
        for i in hours:
            opening_hours.append(i.strip())
        store_address = response.xpath('//p[@class="store-address"]/text()').extract()
        if len(store_address) == 6:
            address = store_address[0].strip()
        else:
            address = '\n'.join([store_address[0].strip(), store_address[1].strip()])
        if data:
            data = json.loads(data)[0]
            name = data.get('name', None)
            name = base64.b64decode(name).decode('utf-8')
            properties = {'ref': data.get('id', None), 'name': name, 'lat': data.get('latitude', None), 'lon': data.get('longitude', None), 'phone': data.get('phone', None), 'addr_full': address, 'state': data.get('stateCode', None), 'city': data.get('city', None), 'country': data.get('countryCode', None), 'postcode': data.get('postalCode', None), 'opening_hours': opening_hours}
            yield Feature(**properties)
    new_property = None
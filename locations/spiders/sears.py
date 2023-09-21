import scrapy
from locations.hours import OpeningHours
from locations.items import Feature

class SearsSpider(scrapy.spiders.SitemapSpider):
    name = 'sears'
    item_attributes = {'brand': 'Sears', 'brand_wikidata': 'Q6499202'}
    allowed_domains = ['www.sears.com']
    sitemap_urls = ['https://www.sears.com/Sitemap_Local.xml.gz']
    sitemap_rules = [('\\d+\\.html$', 'parse')]
    download_delay = 0.3

    def parse(self, response):
        if response.request.meta.get('redirect_urls') and 'store-closed' in response.url:
            return
        oh = OpeningHours()
        for hours_li in response.css('.shc-store-hours')[0].css('li'):
            day, interval = hours_li.css('span::text').extract()
            open_time, close_time = interval.split(' - ')
            oh.add_range(day, open_time, close_time, '%I:%M %p')
        addr_txt = response.css('.shc-store-location__details--address')[0].css('::text').extract()
        street_address, city_postcode = list(filter(None, (s.strip() for s in addr_txt)))
        city, postcode = city_postcode.split(',  ')
        properties = {'ref': response.xpath('//@data-unit-number').get(), 'name': response.xpath('//@data-store-title').get(), 'lat': response.xpath('//@data-latitude').get(), 'lon': response.xpath('//@data-longitude').get(), 'street_address': street_address, 'city': city, 'postcode': postcode, 'state': response.url.split('/')[-3], 'website': response.url, 'phone': response.css('.shc-store-location__details--tel::text').get(), 'opening_hours': oh.as_opening_hours()}
        if 'Hometown' in properties['name']:
            properties.update({'brand': 'Sears Hometown', 'brand_wikidata': 'Q69926963'})
        elif 'Mattress' in properties['name']:
            properties.update({'brand': 'Sears Outlet', 'brand_wikidata': 'Q20080412'})
        yield Feature(**properties)
    requires_proxy = True
    requires_proxy = True
    requires_proxy = True
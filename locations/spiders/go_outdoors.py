from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from locations.google_url import url_to_coords
from locations.linked_data_parser import LinkedDataParser

class GoOutdoorsSpider(CrawlSpider):
    name = 'go_outdoors'
    item_attributes = {'brand': 'Go Outdoors', 'brand_wikidata': 'Q75293941'}
    start_urls = ['https://www.gooutdoors.co.uk/stores']
    rules = [Rule(LinkExtractor(allow='https:\\/\\/www\\.gooutdoors\\.co\\.uk\\/stores\\/([-\\w]+)$'), callback='parse')]

    def parse(self, response):
        store = LinkedDataParser.find_linked_data(response, 'LocalBusiness')
        if store:
            item = LinkedDataParser.parse_ld(store)
            item['name'] = 'Go Outdoors'
            item['ref'] = response.url
            item['website'] = response.url
            item['country'] = 'GB'
            item['lat'], item['lon'] = url_to_coords(store['hasmap'])
            yield item
    new_property = None
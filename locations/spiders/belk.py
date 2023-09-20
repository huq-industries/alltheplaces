from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from locations.structured_data_spider import StructuredDataSpider

class BelkSpider(CrawlSpider, StructuredDataSpider):
    name = 'belk'
    item_attributes = {'brand': 'Belk', 'brand_wikidata': 'Q127428'}
    allowed_domains = ['www.belk.com']
    download_delay = 0.2
    start_urls = ['https://www.belk.com/customer-service/store-directory/']
    rules = [Rule(LinkExtractor(allow='\\/store\\/.+\\/?StoreID=\\d+$'), callback='parse_sd')]
    json_parser = 'json5'
    new_property = None
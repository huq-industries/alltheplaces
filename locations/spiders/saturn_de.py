from scrapy.spiders import SitemapSpider
from locations.structured_data_spider import StructuredDataSpider

class SaturnSpider(SitemapSpider, StructuredDataSpider):
    name = 'saturn_de'
    item_attributes = {'brand': 'Saturn', 'brand_wikidata': 'Q2543504'}
    allowed_domains = ['www.saturn.de']
    sitemap_urls = ['https://www.saturn.de/sitemaps/sitemap-marketpages.xml']
    sitemap_rules = [('/de/store/.+', 'parse_sd')]
    wanted_types = ['Store']
    new_property = None
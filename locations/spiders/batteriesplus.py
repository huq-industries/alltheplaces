import re

import scrapy

from locations.hours import DAYS
from locations.linked_data_parser import LinkedDataParser

daysRe = f"(?:{'|'.join(DAYS)})"


class BatteriesPlusSpider(scrapy.spiders.SitemapSpider):
    name = "batteriesplus"
    item_attributes = {"brand": "Batteries Plus Bulbs", "brand_wikidata": "Q17005157"}
    allowed_domains = ["batteriesplus.com"]
    sitemap_urls = ["https://www.batteriesplus.com/bpb_store-locator_sitemap.xml"]
    sitemap_rules = [("/batteries-plus-", "parse")]

    def parse(self, response):
        if 301 in response.request.meta.get("redirect_reasons", []):
            return
        ld = LinkedDataParser.find_linked_data(response, "ElectronicsStore")
        ld["openingHours"] = re.findall(f"({daysRe}[^A-Z]*) ", ld["openingHours"])
        item = LinkedDataParser.parse_ld(ld)
        item["ref"] = response.url.rsplit("-", 1)[-1]
        yield item

    requires_proxy = True
    requires_proxy = True
    requires_proxy = True

import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from locations.hours import OpeningHours
from locations.structured_data_spider import StructuredDataSpider


class HomeDepotSpider(CrawlSpider, StructuredDataSpider):
    name = "homedepot"
    item_attributes = {"brand": "The Home Depot", "brand_wikidata": "Q864407"}
    allowed_domains = ["www.homedepot.com"]
    start_urls = ["https://www.homedepot.com/l/storeDirectory"]
    rules = [
        Rule(LinkExtractor(allow="^https:\\/\\/www.homedepot.com\\/l\\/..$")),
        Rule(LinkExtractor(allow="^https:\\/\\/www.homedepot.com\\/l\\/.*\\/\\d*$"), callback="parse_sd"),
    ]
    requires_proxy = "US"

    def post_process_item(self, item, response, ld_data, **kwargs):
        data = json.loads(
            response.xpath('//script[contains(text(), "__APOLLO_STATE__")]/text()').extract_first().strip()[24:-1]
        )["ROOT_QUERY"]
        store_info = None
        for k, v in data.items():
            if k.startswith("storeSearch"):
                store_info = v
                break
        if not store_info:
            self.logger.warn("No store_info JSON found in %s", json.dumps(data))
            yield item
        store_info = store_info["stores"][0]
        item["lat"] = store_info["coordinates"]["lat"]
        item["lon"] = store_info["coordinates"]["lng"]
        item["opening_hours"] = OpeningHours()
        for day, info in store_info["storeHours"].items():
            if day == "__typename":
                continue
            item["opening_hours"].add_range(day[:2].title(), info["open"], info["close"])
        yield item

    new_property = None

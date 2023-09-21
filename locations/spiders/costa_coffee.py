from scrapy import Spider
from scrapy.http import JsonRequest

from locations.categories import Categories
from locations.country_utils import CountryUtils
from locations.dict_parser import DictParser
from locations.hours import DAYS_FULL, OpeningHours


class CostaCoffeeSpider(Spider):
    name = "costa_coffee"
    COSTA = {"brand": "Costa Coffee", "brand_wikidata": "Q608845", "extras": Categories.COFFEE_SHOP.value}
    COSTA_EXPRESS = {
        "brand": "Costa Express",
        "brand_wikidata": "Q113556385",
        "extras": Categories.VENDING_MACHINE_COFFEE.value,
    }
    SMART_CAFE = {
        "brand": "Smart Café",
        "brand_wikidata": "Q117448428",
        "extras": Categories.VENDING_MACHINE_COFFEE.value,
    }
    start_urls = [
        "https://www.costa-coffee.be/api/cf/?content_type=storeLocatorStore",
        "https://www.costacoffee.de/api/cf/?content_type=storeLocatorStore",
        "https://www.costacoffee.eg/api/cf/?content_type=storeLocatorStore",
        "https://www.costacoffee.es/api/cf/?content_type=storeLocatorStore",
        "https://www.costacoffee.in/api/cf/?content_type=storeLocatorStore",
        "https://www.costaireland.ie/api/cf/?content_type=storeLocatorStore",
        "https://www.costacoffee.jp/api/cf/?content_type=storeLocatorStore",
        "https://www.costacoffee.ae/api/cf/?content_type=storeLocatorStore",
        "https://us.costacoffee.com/api/cf/?content_type=storeLocatorStore",
    ]
    page_size = 1000
    store_types = {
        "Airport": COSTA,
        "Briggo": None,
        "COFFEEMAKER": {"brand": "Costa Coffee", "extras": Categories.VENDING_MACHINE_COFFEE.value},
        "COSTA EXPRESS": COSTA_EXPRESS,
        "COSTA PARTNER": None,
        "COSTA STORE": COSTA,
        "City": COSTA,
        "Corporate": COSTA,
        "Costa Proud to Serve": None,
        "Hospital": COSTA,
        "Mall": COSTA,
        "Marlow": COSTA,
        "Proud to Serve": None,
        "Smart Café": SMART_CAFE,
        "Store": COSTA,
    }

    def __init__(self):
        self.country_utils = CountryUtils()

    def start_requests(self):
        for url in self.start_urls:
            yield JsonRequest(url=f"{url}&limit={self.page_size}")

    def parse(self, response):
        entries = {}
        for entry in response.json()["includes"]["Entry"]:
            entries[entry["sys"]["id"]] = entry["fields"]["name"]
        if "us.costacoffee.com" in response.url:
            country = "US"
        else:
            country = self.country_utils.country_code_from_url(response.url)
        for location in response.json()["items"]:
            item = DictParser.parse(location["fields"])
            item["ref"] = location["sys"]["id"]
            item["addr_full"] = location["fields"]["storeAddress"]
            item["country"] = country
            item["opening_hours"] = OpeningHours()
            for day_name in [s.lower() for s in DAYS_FULL]:
                open_time = location["fields"].get(f"{day_name}Opening")
                close_time = location["fields"].get(f"{day_name}Closing")
                if open_time and "24 HOURS" in open_time.upper():
                    item["opening_hours"].add_range(day_name, "00:00", "24:00")
                elif open_time and close_time:
                    item["opening_hours"].add_range(day_name, open_time, close_time)
            store_type = entries[location["fields"]["storeType"]["sys"]["id"]]
            if brand := self.store_types.get(store_type):
                item.update(brand)
                yield item
            else:
                self.crawler.stats.inc_value(f"atp/{self.name}/{store_type}/")
        offset = response.json()["skip"]
        if offset + response.json()["limit"] < response.json()["total"]:
            yield JsonRequest(url=f"{response.request.url}&limit={self.page_size}&offset={offset}")

    requires_proxy = True

from scrapy import Spider
from scrapy.http import JsonRequest

from locations.dict_parser import DictParser
from locations.hours import DAYS_NL, OpeningHours
from locations.user_agents import BROWSER_DEFAULT


class AlbertHeijnSpider(Spider):
    name = "albert_heijn"
    item_attributes = {"brand": "Albert Heijn", "brand_wikidata": "Q1653985"}
    allowed_domains = ["www.ah.nl", "www.ah.be"]
    start_urls = ["https://www.ah.nl/gql", "https://www.ah.be/gql"]
    user_agent = BROWSER_DEFAULT

    def get_page(self, gql_url, page_number):
        gql_query = "\nquery stores($filter: StoreFilterInput, $size: PageSize!, $start: Int) {\n  stores(filter: $filter, size: $size, start: $start) {\n    result {\n      ...storeList\n      __typename\n    }\n    page {\n      total\n      hasNextPage\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment storeList on Store {\n  ...storeDetails\n  distance\n  __typename\n}\n\nfragment storeDetails on Store {\n  id\n  name\n  storeType\n  phone\n  address {\n    ...storeAddress\n    __typename\n  }\n  geoLocation {\n    latitude\n    longitude\n    __typename\n  }\n  services {\n    ...serviceInfo\n    __typename\n  }\n  openingDays {\n    ...openingDaysInfo\n    __typename\n  }\n  __typename\n}\n\nfragment storeAddress on StoreAddress {\n  city\n  street\n  houseNumber\n  houseNumberExtra\n  postalCode\n  countryCode\n  __typename\n}\n\nfragment serviceInfo on StoreService {\n  code\n  description\n  shortDescription\n  __typename\n}\n\nfragment openingDaysInfo on StoreOpeningDay {\n  dayName\n  type\n  date\n  nextWeekDate\n  openingHour {\n    ...storeOpeningHour\n    __typename\n  }\n  nextWeekOpeningHour {\n    ...storeOpeningHour\n    __typename\n  }\n  __typename\n}\n\nfragment storeOpeningHour on StoreOpeningHour {\n  date\n  openFrom\n  openUntil\n  __typename\n}\n"
        query = [
            {
                "operationName": "stores",
                "query": gql_query,
                "variables": {"filter": {}, "size": 100, "start": page_number * 100},
            }
        ]
        headers = {
            "client-name": "alltheplaces",
            "client-version": "1",
            "Origin": gql_url.replace("/gql", ""),
            "Referer": gql_url.replace("/gql", "/winkels"),
        }
        yield JsonRequest(url=gql_url, data=query, headers=headers, meta={"page_number": page_number})

    def start_requests(self):
        for url in self.start_urls:
            yield from self.get_page(url, 0)

    def parse(self, response):
        for location in response.json()[0]["data"]["stores"]["result"]:
            item = DictParser.parse(location)
            if ".nl/" in response.url:
                item["website"] = "https://www.ah.nl/winkels?storeId=" + str(item["ref"])
            elif ".be/" in response.url:
                item["website"] = "https://www.ah.be/winkels?storeId=" + str(item["ref"])
            oh = OpeningHours()
            for day in location["openingDays"]:
                if day["dayName"].title() in DAYS_NL and day.get("openingHour"):
                    oh.add_range(
                        DAYS_NL[day["dayName"].title()],
                        day["openingHour"]["openFrom"],
                        day["openingHour"]["openUntil"],
                        "%H:%M",
                    )
            item["opening_hours"] = oh.as_opening_hours()
            yield item
        if response.json()[0]["data"]["stores"]["page"]["hasNextPage"]:
            yield from self.get_page(response.url, response.meta["page_number"] + 1)

    requires_proxy = True
    requires_proxy = True
    requires_proxy = True

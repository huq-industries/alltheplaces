import base64
import json
import time

import scrapy

from locations.hours import OpeningHours
from locations.items import Feature


class RalphLaurenSpider(scrapy.Spider):
    name = "ralph_lauren"
    allowed_domains = ["www.ralphlauren.com"]
    start_urls = ("https://www.ralphlauren.com/Stores-ShowCountries",)
    # start_urls = ("https://www.ralphlauren.com/Stores-Details?StoreID=474",)

    def parse(self, response):
        # gather URLs of all countries
        countries = response.xpath('//a[@class="store-directory-countrylink"]/@href').extract()

        for country in countries:
            # build URL for per country overview of all stores, countrycode is after the equals sign, e.g. /Stores-ShowStates?countryCode=US
            url = (
                "/findstores?dwfrm_storelocator_country="
                + (country.split("=", 1)[1])
                + "&dwfrm_storelocator_findbycountry=Search&findByValue=CountrySearch"
            )
            yield scrapy.Request(response.urljoin(url), callback=self.parse_city)

    def parse_city(self, response):
        # get all stores per country
        stores = response.xpath('//span[@class="store-listing-name"]/a/@href').extract()

        for store in stores:
            yield scrapy.Request(response.urljoin(store), callback=self.parse_locations)

    def parse_locations(self, response):
        # get json which provides most of the data
        data = response.xpath('//div[@class="storeJSON hide"]/@data-storejson').extract_first()

        # opening hours are not in json, thus need to be scraped separately
        hours = response.xpath('//tr[@class="store-hourrow"]//td//text()').getall()
        opening_hours = OpeningHours()

        # a few stores have a slightly different format with no : and more whitespace
        if len(hours) > 7:
            hours = [f"{i}: {j}" for i, j in zip(hours[::2], hours[1::2])]

        for h in hours:
            hours_text = h.replace(" ", "")
            day = hours_text[:3]
            for session in hours_text[4:].split(","):
                if session == "CLOSED":
                    continue
                hrs = [time.strptime(t.zfill(7), "%I:%M%p") for t in session.split("-")]
                opening_hours.add_range(day, hrs[0], hrs[1])

        # some stores have a second address line which is not in the json
        store_address = response.xpath('//div[@class="store-info-container"]/div/span/text()').extract()
        stripped_address = [s.strip() for s in store_address]
        # last two elements are ["City, ST ZIP", "Country"]
        street_address = ", ".join(stripped_address[:-2])

        if data:
            data = json.loads(data)[0]

            # decode base64 string
            name = data.get("name", None)
            name = base64.b64decode(name).decode("utf-8")

            properties = {
                "ref": data.get("id", None),
                "name": name,
                "lat": data.get("latitude", None),
                "lon": data.get("longitude", None),
                "phone": data.get("phone", None),
                "street_address": street_address,
                "state": data.get("stateCode", None),
                "city": data.get("city", None),
                "country": data.get("countryCode", None),
                "postcode": data.get("postalCode", None),
                "opening_hours": opening_hours,
                "extras": {
                    "full_address": stripped_address,
                },
            }

            yield Feature(**properties)

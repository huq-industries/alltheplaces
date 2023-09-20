import scrapy
from locations.dict_parser import DictParser
from locations.hours import DAYS, OpeningHours
from locations.user_agents import BROWSER_DEFAULT

class InditexSpider(scrapy.Spider):
    name = 'inditex'
    my_brands = {'bershka': {'brand': 'Bershka', 'brand_wikidata': 'Q827258'}, 'massimodutti': {'brand': 'Massimo Dutti', 'brand_wikidata': 'Q788231'}, 'oysho': {'brand': 'Oysho', 'brand_wikidata': 'Q3327046'}, 'zarahome': {'brand': 'Zara Home', 'brand_wikidata': 'Q3114054'}, 'stradivarius': {'brand': 'Stradivarius', 'brand_wikidata': 'Q3322945'}, 'pullandbear': {'brand': 'Pull&Bear', 'brand_wikidata': 'Q691029'}, 'lefties': {'brand': 'Lefties', 'brand_wikidata': 'Q12391713'}}
    start_urls = ['https://www.massimodutti.com/itxrest/2/web/seo/config?appId=1']
    custom_settings = {'ROBOTSTXT_OBEY': False}
    user_agent = BROWSER_DEFAULT
    download_delay = 2.0

    def parse(self, response):
        config = response.json()['seoParamMap']
        for store_id, country in config['storeId'].items():
            brand = config['brandId'][store_id[0]]
            if brand == 'dutti':
                brand = 'massimodutti'
            if brand == 'uterque':
                continue
            url = 'https://www.{}.com/itxrest/2/bam/store/{}/physical-stores-by-country?countryCode={}'.format(brand, store_id, country.upper())
            yield scrapy.http.JsonRequest(url, callback=self.parse_stores, cb_kwargs=dict(brand=brand))

    def parse_stores(self, response, brand):
        for store in response.json()['stores']:
            item = DictParser.parse(store)
            item['website'] = 'https://www.{}.com/'.format(brand) + item['country'].lower()
            item.update(self.my_brands.get(brand))
            item['phone'] = store.get('phones', [None])[0]
            item['street_address'] = store['addressLines'][0]
            oh = OpeningHours()
            for record in store['openingHours']['schedule']:
                for day in record['weekdays']:
                    oh.add_range(DAYS[day - 1], record['timeStripList'][0]['initHour'], record['timeStripList'][0]['endHour'])
            yield item
    new_property = None
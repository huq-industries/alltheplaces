from scrapy.http import JsonRequest
from scrapy.spiders import CSVFeedSpider
from locations.dict_parser import DictParser

class GBFSSpider(CSVFeedSpider):
    name = 'gbfs'
    start_urls = ['https://github.com/MobilityData/gbfs/raw/master/systems.csv']
    custom_settings = {'ROBOTSTXT_OBEY': False}

    def parse_row(self, response, row):
        yield JsonRequest(url=row['Auto-Discovery URL'], cb_kwargs=row, callback=self.parse_gbfs)

    def parse_gbfs(self, response, **kwargs):
        try:
            data = response.json()
        except:
            return
        for feed in DictParser.get_nested_key(data, 'feeds') or []:
            if feed['name'] == 'station_information':
                yield JsonRequest(url=feed['url'], cb_kwargs=kwargs, callback=self.parse_stations)

    def parse_stations(self, response, **kwargs):
        try:
            data = response.json()
        except:
            return
        for station in DictParser.get_nested_key(data, 'stations') or []:
            station['id'] = kwargs['System ID'] + '-' + str(station['station_id'])
            if station.get('address'):
                station['street_address'] = station.pop('address')
            station['country'] = kwargs['Country Code']
            item = DictParser.parse(station)
            item['brand'] = kwargs['Name']
            item['extras']['capacity'] = station.get('capacity')
            item['website'] = kwargs['URL']
            item['extras']['public_transport'] = 'stop_position'
            yield item
    new_property = None
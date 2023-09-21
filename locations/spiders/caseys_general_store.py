from scrapy.spiders import SitemapSpider

from locations.linked_data_parser import LinkedDataParser


class CaseysGeneralStoreSpider(SitemapSpider):
    name = "caseys_general_store"
    item_attributes = {"brand": "Casey's General Store", "brand_wikidata": "Q2940968"}
    allowed_domains = ["www.caseys.com"]
    sitemap_urls = ["https://www.caseys.com/sitemap.xml"]
    sitemap_follow = ["https://www.caseys.com/medias/sys_master/root/.*/Store-en-USD-.*.xml"]
    sitemap_rules = [("https://www.caseys.com/general-store/.*/[0-9]*", "parse")]
    requires_proxy = True

    def parse(self, response):
        item = LinkedDataParser.parse(response, "ConvenienceStore")
        item["ref"] = item["website"].split("/")[-1]
        yield item

    requires_proxy = True

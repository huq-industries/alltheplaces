import json
import os
from datetime import datetime

from scrapy import Spider


def feed_uri_params(params, spider: Spider):
    return {
        **params,
        "env": spider.settings.get("ENV"),
        "bucket": spider.settings.get("GCS_BUCKET"),
        "schedule_date": spider.settings.get("SCHEDULE_DATE"),
        "spider_name": spider.name,
    }

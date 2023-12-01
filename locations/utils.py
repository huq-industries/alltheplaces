import json
import os
from datetime import datetime

from scrapy import Spider


def feed_uri_params(params, spider: Spider):
    job_data = json.loads(os.environ.get("JOB_DATA", "{}"))

    return {
        **params,
        "env": spider.settings.get("ENV"),
        "bucket": spider.settings.get("GCS_BUCKET"),
        "schedule_date": os.environ.get("SCHEDULE_DATE"),
        "spider_name": spider.name,
    }

from __future__ import annotations

import traceback
import warnings
from collections import defaultdict
from types import ModuleType
from typing import TYPE_CHECKING, DefaultDict, Dict, List, Tuple, Type

from scrapy import Request, Spider
from scrapy.settings import BaseSettings
from scrapy.spiderloader import SpiderLoader
from scrapy.utils.misc import walk_modules
from scrapy.utils.spider import iter_spider_classes

if TYPE_CHECKING:
    # typing.Self requires Python 3.11
    from typing_extensions import Self


class HuqSpiderLoader(SpiderLoader):
    """
    HuqSpiderLoader is a class which locates and loads spiders
    in a Scrapy project.
    """
    def list_schedule(self) -> Dict:
        """
        Return a dict with the names of all spiders available in the project and their scheduling config.
        """
        return {
            k: {
                "priority": getattr(v, "zyte_priority", 0),
                "units": getattr(v, "zyte_units", 1),
            }
            for k, v in self._spiders.items()
        }

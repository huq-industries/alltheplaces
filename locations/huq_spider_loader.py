from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from scrapy.spiderloader import SpiderLoader

if TYPE_CHECKING:
    # typing.Self requires Python 3.11
    pass


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

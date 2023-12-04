import subprocess
from datetime import date

from scrapy.commands import ScrapyCommand


class Command(ScrapyCommand):
    requires_project = True
    default_settings = {"LOG_ENABLED": False}

    def short_desc(self):
        return "Schedule available spiders"

    def run(self, args, opts):
        schedule_date = date.today().isoformat()
        project = args[0] if len(args) > 0 else "default"
        spiders = self.crawler_process.spider_loader.list_schedule()

        for spider, conf in spiders.items():
            result = subprocess.run(
                [
                    "pipenv", "run", "shub", "schedule",
                    "--priority", str(conf["priority"]),
                    "--units", str(conf["units"]),
                    "--set", f"SCHEDULE_DATE={schedule_date}",
                    f"{project}/{spider}"
                ]
            )
            result.check_returncode()

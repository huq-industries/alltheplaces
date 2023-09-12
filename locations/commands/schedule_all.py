import subprocess

from scrapy.commands import ScrapyCommand


class Command(ScrapyCommand):
    requires_project = True
    default_settings = {"LOG_ENABLED": False}

    def short_desc(self):
        return "Schedule available spiders"

    def run(self, args, opts):
        spiders = self.crawler_process.spider_loader.list_schedule()
        # Priority 0 while we only have one container group - dev spiders will run first
        for spider, units in spiders.items():
            subprocess.run(["pipenv", "run", "shub", "schedule", "-p 0", f"-u {units}", f"prod/{spider}"])

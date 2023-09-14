import subprocess

from scrapy.commands import ScrapyCommand


class Command(ScrapyCommand):
    requires_project = True
    default_settings = {"LOG_ENABLED": False}

    def short_desc(self):
        return "Schedule available spiders"

    def run(self, args, opts):
        project = args[0] if len(args) > 0 else "default"

        spiders = self.crawler_process.spider_loader.list_schedule()
        for spider, conf in spiders.items():
            priority = conf["priority"]
            units = conf["units"]
            subprocess.run(
                ["pipenv", "run", "shub", "schedule", f"-p {priority}", f"-u {units}", f"{project}/{spider}"]
            )

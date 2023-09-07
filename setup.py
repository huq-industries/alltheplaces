# Automatically created by: shub deploy

from setuptools import find_packages, setup

setup(
    name="alltheplaces",
    version="1.0",
    packages=find_packages(),
    entry_points={"scrapy": ["settings = locations.settings"]},
    include_package_data=True,
)

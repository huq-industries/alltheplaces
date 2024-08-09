import os

ENV = "production"  # "production" or "local"

# GCS CONFIGS
BUCKET_NAME = os.getenv("BUCKET_NAME", "huq-osm")
ZIP_STORAGE_PATH = os.getenv("ZIP_STORAGE_PATH", "test/atp_storage")
OUTPUT_PATH = os.getenv("OUTPUT_PATH", f"alltheplaces/{ENV}")

# ATP CONFIGS
ATP_URL = "https://data.alltheplaces.xyz/runs/latest.json"
ATP_REPO = os.getenv("ATP_REPO", "huq-industries/alltheplaces")
ATP_REPO_PATH = os.getenv("ATP_REPO_PATH", "locations/spiders")
GITHUB_TOKEN = os.getenv(
    "GITHUB_TOKEN",
    "",
)

# Add any other configuration variables here
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 5))

from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())

TOKEN = os.environ.get("TOKEN")
WEBHOOK_HOST = os.environ.get("WEBHOOK_HOST")
# WEBHOOK_PATH = f"/bot{TOKEN}"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
DB_LITE = os.environ.get("DB_LITE")


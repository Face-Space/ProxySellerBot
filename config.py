from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())

TOKEN = os.environ.get("TOKEN")
WEBHOOK_HOST = os.environ.get("WEBHOOK_HOST")
# WEBHOOK_PATH = f"/bot{TOKEN}"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
DB_LITE = os.environ.get("DB_LITE")
PAYMENT_TOKEN = os.environ.get("PAYMENT_TOKEN")
ADMIN_ID_LIST_RAW = os.environ.get("ADMIN_ID_LIST").split(",")
ADMIN_ID_LIST = [int(admin_id) for admin_id in ADMIN_ID_LIST_RAW]
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
REDIS_HOST = os.environ.get("REDIS_HOST")

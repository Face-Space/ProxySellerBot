from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())

TOKEN = os.environ.get("TOKEN")
BASE_URL = os.getenv("AMVERA_APP_URL")
WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{BASE_URL}{WEBHOOK_PATH}"
WEBHOOK_SECRET_TOKEN = os.getenv("WEBHOOK_SECRET_TOKEN")
DB_LITE = os.environ.get("DB_LITE")
DB_URL = os.environ.get("DB_URL")
PAYMENT_TOKEN = os.environ.get("PAYMENT_TOKEN")
ADMIN_ID_LIST_RAW = os.environ.get("ADMIN_ID_LIST").split(",")
ADMIN_ID_LIST = [int(admin_id) for admin_id in ADMIN_ID_LIST_RAW]
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
REDIS_HOST = os.environ.get("REDIS_HOST")
CRYPTO_PAY_TOKEN = os.environ.get("CRYPTO_PAY_TOKEN")
PAGE_ENTRIES = int(os.environ.get("PAGE_ENTRIES"))
KRYPTO_EXPRESS_API_SECRET = os.environ.get("KRYPTO_EXPRESS_API_SECRET")
KRYPTO_EXPRESS_API_KEY = os.environ.get("KRYPTO_EXPRESS_API_KEY")
KRYPTO_EXPRESS_API_URL = os.environ.get("KRYPTO_EXPRESS_API_URL")
DJANGO_SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")


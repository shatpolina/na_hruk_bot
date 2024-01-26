from dotenv import load_dotenv
import os

load_dotenv('.env')

BOT_TOKEN = os.getenv("BOT_TOKEN")
if BOT_TOKEN is None:
    print('For work I need BOT_TOKEN in .env')
    quit()

DB_LOCATION = os.getenv("DB_LOCATION")
ADMIN = os.getenv("ADMIN")

SUCCESS_INSERT_MESSAGE = os.getenv("SUCCESS_INSERT_MESSAGE")
FAILED_INSERT_MESSAGE = os.getenv("FAILED_INSERT_MESSAGE")
EMPTY_DB_MESSAGE = os.getenv("EMPTY_DB_MESSAGE")
NON_HRUK_MESSAGE = os.getenv("NON_HRUK_MESSAGE")
UNAUTHORIZED_ACCESS_MESSAGE = os.getenv("UNAUTHORIZED_ACCESS_MESSAGE")

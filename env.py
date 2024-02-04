from dotenv import load_dotenv
import os
from random import randrange

load_dotenv('.env')

BOT_TOKEN = os.getenv("BOT_TOKEN")
if BOT_TOKEN is None:
    print('For work I need BOT_TOKEN in .env')
    quit()

DB_LOCATION = os.getenv("DB_LOCATION")
if DB_LOCATION is None:
    print('For work I need DB_LOCATION in .env')
    quit()

ADMIN = os.getenv("ADMIN")

RATE_LIMIT = 5
RATE_LIMIT_TIME = 3600
# I know how LOOOOOONG the names of these vars are
RATE_LIMIT_RATE_LIMIT = 3
RATE_LIMIT_TIME_RATE_LIMIT_TIME = 3600

SUCCESS_INSERT_MESSAGE = os.getenv("SUCCESS_INSERT_MESSAGE")
FAILED_INSERT_MESSAGE = os.getenv("FAILED_INSERT_MESSAGE")
SUCCESS_DELETE_MESSAGE = os.getenv("SUCCESS_DELETE_MESSAGE")
FAILED_DELETE_MESSAGE = os.getenv("FAILED_DELETE_MESSAGE")
EMPTY_DB_MESSAGE = os.getenv("EMPTY_DB_MESSAGE")
NON_HRUK_MESSAGE_LIST = os.getenv("NON_HRUK_MESSAGE").split(";")
UNAUTHORIZED_ACCESS_MESSAGE = os.getenv("UNAUTHORIZED_ACCESS_MESSAGE")
RATE_LIMIT_MESSAGE_LIST = os.getenv("RATE_LIMIT_MESSAGE").split(";")


def rate_limit_message(i: int) -> str:
    sec = 'секунд'
    d = int(str(i)[-1])
    if d in [2, 3, 4]:
        sec = 'секунды'
    if d == 1:
        sec = 'секунду'
    rand = randrange(len(RATE_LIMIT_MESSAGE_LIST))
    return f'{RATE_LIMIT_MESSAGE_LIST[rand]} {i} {sec}'

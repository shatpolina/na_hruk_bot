import telebot
import env
from ratelimit import limits, RateLimitException
from db_handler import Database
from random import randrange


bot = telebot.TeleBot(env.BOT_TOKEN)
db_file = env.DB_LOCATION


@bot.message_handler(commands=['h', 'hruk'])
def echo_hruk(msg):
    send_hruk(msg)


@bot.message_handler(commands=['newhruk'])
def echo_new_hruk(msg):
    if f'{msg.from_user.id}' in env.ADMIN:
        new_gif(msg)
    else:
        bot.reply_to(message=msg, text=env.UNAUTHORIZED_ACCESS_MESSAGE)


@bot.message_handler(commands=['delhruk'])
def echo_del_hruk(msg):
    if f'{msg.from_user.id}' in env.ADMIN:
        del_gif(msg)
    else:
        bot.reply_to(message=msg, text=env.UNAUTHORIZED_ACCESS_MESSAGE)


@bot.message_handler(func=lambda m: True)
def echo_all(msg):
    if "хрю" in msg.text.lower():
        send_hruk(msg)


def send_hruk(msg):
    print("ECHO HRUK")
    try:
        print("IN TRY BEFORE SEND GIF")
        send_gif(msg)
    except RateLimitException as e:
        try:
            text = f'{env.rate_limit_message(int(e.period_remaining))}'
            bot.reply_to(message=msg, text=text)
        except RateLimitException as e:
            print('rate limit to rate limit messaging ', e.period_remaining)


@limits(calls=env.RATE_LIMIT, period=env.RATE_LIMIT_TIME)
def send_gif(msg):
    with Database(db_file) as db:
        file_id = db.select_random_gif()
        print(f'SEND GIF {file_id}')
    if file_id:
        bot.send_animation(
            chat_id=msg.chat.id,
            animation=file_id,
        )
    else:
        bot.reply_to(message=msg, text=env.EMPTY_DB_MESSAGE)


def new_gif(msg):
    repl = msg.reply_to_message
    match repl.content_type:
        case 'animation':
            file_id = repl.animation.file_id
            file_unique_id = repl.animation.file_unique_id
            with Database(db_file) as db:
                insert = db.insert(file_id, file_unique_id)
            result = env.SUCCESS_INSERT_MESSAGE if insert else env.FAILED_INSERT_MESSAGE
        case _:
            # TODO: check gif to non-hruk content
            result = env.NON_HRUK_MESSAGE_LIST[randrange(
                len(env.NON_HRUK_MESSAGE_LIST))]
    bot.reply_to(message=msg, text=result)


def del_gif(msg):
    repl = msg.reply_to_message
    match repl.content_type:
        case 'animation':
            file_unique_id = repl.animation.file_unique_id
            with Database(db_file) as db:
                res = db.delete(file_unique_id)
            result = env.SUCCESS_DELETE_MESSAGE if res else env.FAILED_DELETE_MESSAGE
        case _:
            # TODO: check gif to non-hruk content
            result = env.NON_HRUK_MESSAGE_LIST[randrange(
                len(env.NON_HRUK_MESSAGE_LIST))]
    bot.reply_to(message=msg, text=result)


bot.infinity_polling()

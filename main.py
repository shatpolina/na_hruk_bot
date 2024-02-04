import telebot
import env
from ratelimit import limits, RateLimitException
from db_handler import Database
from random import randrange


bot = telebot.TeleBot(env.BOT_TOKEN)
db_file = env.DB_LOCATION
chat_limits = {}


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


def rate_limit_handler(key, fn, calls, period, *args, **kargs):
    global chat_limits
    key = key + (fn.__name__, )
    if chat_limits.get(key) is None:
        chat_limits.update(
            {key: limits(calls=calls, period=period)})
    return chat_limits.get(key)(fn)(*args, **kargs)


def send_hruk(msg):
    print("ECHO HRUK")
    key = (msg.chat.id, msg.from_user.id)
    try:
        print("IN TRY BEFORE SEND with limits")
        rate_limit_handler(key, send_gif, env.RATE_LIMIT,
                           env.RATE_LIMIT_TIME, msg)
    except RateLimitException as e:
        try:
            # I know how LOOOOOONG the names of these vars are
            res = rate_limit_handler(key, env.rate_limit_message, env.RATE_LIMIT_RATE_LIMIT,
                                     env.RATE_LIMIT_TIME_RATE_LIMIT_TIME, int(e.period_remaining))
            bot.reply_to(message=msg, text=f'{res}')
        except RateLimitException as e:
            print('rate limit to rate limit messaging ', e.period_remaining)


def send_gif(msg):
    with Database(db_file) as db:
        file_id = db.select_random_gif()
    if file_id:
        print(f'SEND GIF {file_id}')
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

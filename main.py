import telebot
import env
from db_handler import Database


bot = telebot.TeleBot(env.BOT_TOKEN, parse_mode=None)
db_file = env.DB_LOCATION


@bot.message_handler(commands=['h', 'hruk'])
def echo_hruk(msg):
    if msg.reply_to_message:
        new_gif(msg)
    else:
        send_gif(msg)


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
                insert = db.insert_gif(file_id, file_unique_id)
            result = env.SUCCESS_INSERT_MESSAGE if insert else env.FAILED_INSERT_MESSAGE
        case _:
            # TODO: check gif to non-hruk content
            result = 'Принимаю только гифки c поросями, убери свою ересь'
    bot.reply_to(message=msg, text=result)


bot.infinity_polling()

import os

import telebot
from telebot import types

from dotenv import load_dotenv

from BaseHandler import BaseHandler
from FetchDataHander import FetchDataHandler
from SimpleHandler import SimpleHandler
from EditPetHandler import EditPetHandler

load_dotenv(".env")
load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))

BACKEND_URL = os.getenv("BACKEND_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

base_handler = BaseHandler(bot, BACKEND_URL)
simple_handler = SimpleHandler(base_handler)
fetch_data_handler = FetchDataHandler(base_handler)
edit_pet_handler = EditPetHandler(base_handler)

base_handler.menu_handlers = [
    *simple_handler.handlers,
    *fetch_data_handler.handlers,
    *edit_pet_handler.handlers,
]


@bot.message_handler(commands=['start'])
def start_menu(message):
    base_handler.start(message.chat.id)


def reply_filter(msg):
    return msg.reply_to_message is not None


@bot.message_handler(func=reply_filter)
def reply_msg_handler(msg):
    chat_id = msg.chat.id
    user_id = msg.from_user.id
    reply_text = msg.reply_to_message.text
    found_handler_arr = list(filter(
        lambda item: item["text"] == reply_text,
        [
            *fetch_data_handler.query_handlers,
            *edit_pet_handler.query_handlers,
        ],
    ))
    if len(found_handler_arr) > 0:
        found_handler_arr[0]["handler"](chat_id, user_id, msg.text)


@bot.message_handler(func=lambda call: True)
def default_msg_handler(msg):
    markup = types.ReplyKeyboardRemove(selective=True)
    chat_id = msg.chat.id
    user_id = msg.from_user.id
    bot.send_message(chat_id, msg.text, reply_markup=markup)
    found_handler_arr = list(filter(
        lambda item: item["text"] == msg.text,
        base_handler.menu_handlers,
    ))
    if len(found_handler_arr) > 0:
        found_handler_arr[0]["handler"](chat_id, user_id)


bot.infinity_polling()

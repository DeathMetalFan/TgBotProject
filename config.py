BOT_TOKEN = '6201498048:AAGYuffOZwzZiDJeWkJ727_Uaq6VJzVOjb8'

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot(BOT_TOKEN) # заменить "token" на токен своего бота

clv_1 = ReplyKeyboardMarkup(resize_keyboard=True)
btn_1 = KeyboardButton('Ввести цвет 1')
btn_2 = KeyboardButton('Ввести цвет 2')
clv_1.row(btn_1, btn_2)

color_1 = None
color_2 = None

@bot.message_handler(func=lambda message: message.text == "Ввести цвет 1")
def send_color_1(message):
    global color_1
    bot.send_message(chat_id=message.chat.id, text="Введите цвет 1:")
    color_1 = message.text

@bot.message_handler(func=lambda message: message.text == "Ввести цвет 2")
def send_color_2(message):
    global color_2
    bot.send_message(chat_id=message.chat.id, text="Введите цвет 2:")
    color_2 = message.text

import os
import telebot
from telebot import types
from config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)
help_message = 'Этот бот может генерировать изображения по заданному вами тексту, а также посоветовать альбом или предложить музыкальную новинку.'


@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    create_img_button = types.KeyboardButton('Сгенерируй изображение')
    recommend_music_button = types.KeyboardButton('Посоветуй какую-нибудь музыку')
    novas_in_music_button = types.KeyboardButton('Какие новинки в мире музыки?')
    help_button = types.KeyboardButton('/help')
    markup.add(create_img_button, recommend_music_button, novas_in_music_button, help_button)

    user_name = message.chat.username
    folder_path = os.path.join(os.getcwd(), 'usercache', user_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    bot.send_message(
        message.chat.id,
        f'Доброго времени суток. {help_message}',
        reply_markup=markup
    )


@bot.message_handler(commands=['Сгенерируй изображение'])
def img_generate(message):



@bot.message_handler(commands=['help'])
def help_handler(message):
    user_id = message.chat.id
    bot.send_message(user_id, help_message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
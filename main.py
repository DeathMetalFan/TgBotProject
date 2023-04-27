import os
import logging
from telegram.ext import Application, MessageHandler, CommandHandler, filters
from telegram import ReplyKeyboardMarkup
from config import BOT_TOKEN


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


bot = Application.builder().token(BOT_TOKEN).build()
help_message = 'Этот бот может генерировать изображения по заданному вами тексту, а также посоветовать альбом или предложить музыкальную новинку.'
color_1 = None
color_2 = None


async def start_function(update, context):
    user = update.effective_user
    reply_keyboard = [['/img_gen', '/music_tip', '/news_music', '/help']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    folder_path = os.path.join(os.getcwd(), 'usercache', user.username)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    await update.message.reply_text(help_message, reply_markup=markup)


async def img_generator(update, context):
    user = update.effective_user
    reply_keyboard =[['/change_text_color', '/change_bg_color']]


# @bot.message_handler(func=lambda message: message.text == 'Сгенерируй изображение')
# def img_generate(message):
#     color_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     color_bg_button = types.KeyboardButton('Задать цвет фона')
#     color_txt_button = types.KeyboardButton('Задать цвет текста')
#     color_markup.row(color_bg_button, color_txt_button)
#     bot.send_message(message.chat.id, 'Хорошо, только, сперва, задайте цвета.', reply_markup=color_markup)
#
#
# @bot.message_handler(func=lambda message: message.text == "Задать цвет фона")
# def send_color_1(message):
#     global color_1
#     bot.send_message(chat_id=message.chat.id,
#                      text="Задайте цвет фона. Вы можете использовать как RGB формат записи цвета, так и шестнадцатеричный, или просто написать цвет словами.")
#     color_1 = message.text
#     print(color_1)
#
#
# @bot.message_handler(func=lambda message: message.text == "Задать цвет текста")
# def send_color_2(message):
#     global color_2
#     bot.send_message(chat_id=message.chat.id,
#                      text="Задайте цвет текста. Вы можете использовать как RGB формат записи цвета, так и шестнадцатеричный, или просто написать цвет словами.")
#     color_2 = message.text
#     print(color_2)


async def help_function(update, contexxt):
    await update.message.reply_text(help_message)


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    bot = Application.builder().token(BOT_TOKEN).build()

    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    start_handler = CommandHandler('start', start_function)
    help_handler = CommandHandler('help', help_function)


    # Регистрируем обработчик в приложении.
    bot.add_handler(start_handler)
    bot.add_handler(help_handler)

    # Запускаем приложение.
    bot.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
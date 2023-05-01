from datetime import datetime
import os
import logging
import csv
from telegram.ext import Application, MessageHandler, CommandHandler, filters
from telegram import ReplyKeyboardMarkup
from random import choice
from config import BOT_TOKEN
from img_generation import generate
import sqlalchemy

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

bot = Application.builder().token(BOT_TOKEN).build()
help_message = 'Этот бот может генерировать изображения по заданному вами тексту, а также посоветовать альбом или предложить музыкальную новинку.' \
               '\nДля генерации изображения введите команду /img_gen [желаемый текст] [цвет текста] [цвет фона]' \
               '\nВы можете вводить цвета в шестнадцатеричном, или в RGB-формате. Цвет текста по умолчанию белый, цвет фона - чёрный.'


async def start_function(update, context):
    user = update.effective_user
    reply_keyboard = [['/img_gen', '/music_tip', '/news_music', '/help']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    folder_path = os.path.join(os.getcwd(), 'usercache', user.username)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        with open(f'{folder_path}/color_cache.csv', 'w', newline='', encoding='utf8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([(0, 0, 0), (255, 255, 255)])
    await update.message.reply_text(f'Доброго времения суток. \n{help_message}', reply_markup=markup)


async def img_generator(update, context):
    user = update.effective_user
    message_data = update.message.text.split('[')[1::]
    if ' '.join(message_data).count(']') != 3:
        await update.message.reply_text('Упс, вы ошиблись при вводе параметров!')
    else:
        text = ''.join([i for i in message_data[0] if i != ']'])[:-1:]
        color_text = ''.join([i for i in message_data[1] if i != ']'])
        color_bg = ''.join([i for i in message_data[2] if i != ']'])
        if color_text[0] != '#':
            color_fst, color_scd = int(color_text.split()[0][:-1:]), int(color_text.split()[1][:-1:])
            color_trd = int(color_text.split()[2])
            color_text = tuple([color_fst, color_scd, color_trd])
        if color_bg[0] != '#':
            color_fst, color_scd = int(color_bg.split()[0][:-1:]), int(color_bg.split()[1][:-1:])
            color_trd = int(color_bg.split()[2])
            color_bg = tuple([color_fst, color_scd, color_trd])
        image = generate(text, color_text, color_bg)
        image_name = f'{datetime.now()}.png'
        image_path = f'usercache/{user.username}/{image_name}'
        image.save(image_path)
        await context.bot.send_photo(chat_id=update.message.chat_id, photo=open(image_path, 'rb'))


async def help_function(update, context):
    await update.message.reply_text(help_message)


def main():
    # Создаём объект Application.
    bot = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчик в приложении.
    bot.add_handler(CommandHandler('start', start_function))
    bot.add_handler(CommandHandler('help', help_function))
    bot.add_handler(CommandHandler('img_gen', img_generator))

    # Запускаем приложение.
    bot.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()

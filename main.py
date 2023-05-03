from datetime import datetime
import os
import logging
import csv
from telegram.ext import Application, CommandHandler
from telegram import ReplyKeyboardMarkup
from random import choice
from config import BOT_TOKEN
from img_generation import generate
import sqlite3


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
    reply_keyboard = [['/img_gen', '/music_tip', '/help']]
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

    # Получаем аргументы команды
    message_data = update.message.text.split('[')[1::]

    # Проверяем правильность введённых параметров
    if ' '.join(message_data).count(']') != 3:
        await update.message.reply_text('Упс, вы ошиблись при вводе параметров!')
    else:

        # Если всё правильно - отдёляем части команды друг от друга
        text = ''.join([i for i in message_data[0] if i != ']'])[:-1:]
        color_text = ''.join([i for i in message_data[1] if i != ']'])
        color_bg = ''.join([i for i in message_data[2] if i != ']'])

        # Форматируем переданные цвета
        # Проверяем, в какой системе записан цвет текста...
        if color_text[0] != '#':
            color_fst, color_scd = int(color_text.split()[0][:-1:]), int(color_text.split()[1][:-1:])
            color_trd = int(color_text.split()[2])
            color_text = tuple([color_fst, color_scd, color_trd])

        # ...и цвет фона
        if color_bg[0] != '#':
            color_fst, color_scd = int(color_bg.split()[0][:-1:]), int(color_bg.split()[1][:-1:])
            color_trd = int(color_bg.split()[2])
            color_bg = tuple([color_fst, color_scd, color_trd])

        # Создаём изображение
        image = generate(text, color_text, color_bg)

        # Сохраняем изображение в папке пользователя с именем в формате ГГММДД_чч-мм-сс
        dt_now = datetime.now()
        image_name = f'{dt_now.strftime("%Y%m%d_%H-%M-%S")}.png'
        image_path = f'usercache/{user.username}/{image_name}'
        image.save(image_path)

        # Отправляем изображение пользователю
        await context.bot.send_photo(chat_id=update.message.chat_id, photo=open(image_path, 'rb'))


async def help_function(update, context):
    # Вывод подсказки
    await update.message.reply_text(help_message)


async def recommend_function(update, context):
    user = update.effective_user

    # Подключение к БД
    connection = sqlite3.connect(f'static{os.sep}db{os.sep}music.sqlite')

    # Создание курсора
    cursor = connection.cursor()

    # Получаем имя случайного альбома
    album_name = choice([i[0] for i in cursor.execute('''SELECT name FROM Albums''').fetchall()])

    # Выполнение запроса и получение всех результатов
    album_author, album_year, album_genre, cover_link, album_link = cursor.execute(f'''SELECT author, year, genre, cover_link, album_link FROM Albums WHERE name = "{album_name}"''').fetchall()[0]
    
    text = f'{album_author} - {album_name}\n' \
           f'{album_year}\n' \
           f'{album_genre}\n' \
           f'Ссылка на альбом - {album_link}'
    filename = f'{cover_link}'
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=open(filename, 'rb'), caption=text)


def main():

    # Создаём объект Application.
    bot = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчики в приложении.
    bot.add_handler(CommandHandler('start', start_function))
    bot.add_handler(CommandHandler('help', help_function))
    bot.add_handler(CommandHandler('img_gen', img_generator))
    bot.add_handler(CommandHandler('music_tip', recommend_function))

    # Запускаем приложение.
    bot.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()

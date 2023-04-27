import os
import logging
import csv
from telegram.ext import Application, MessageHandler, CommandHandler, filters
from telegram import ReplyKeyboardMarkup
from random import choice
from config import BOT_TOKEN
from img_genration import generate

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

bot = Application.builder().token(BOT_TOKEN).build()
help_message = 'Этот бот может генерировать изображения по заданному вами тексту, а также посоветовать альбом или предложить музыкальную новинку.'


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
    await update.message.reply_text(help_message, reply_markup=markup)


async def img_generator(update, context):
    user = update.effective_user
    reply_keyboard = [['/change_text_color 255 255 255', '/change_bg_color 0 0 0']]
    await update.message.reply_text('Выберите цвет шрифта и цвет фона:',
                                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


async def change_bg(update, context):  # Функция по изменения цвета фона
    user = update.effective_user
    folder_path = os.path.join(os.getcwd(), 'usercache', user.username)

    # Открываем файл в формате read и берём цвет текста
    with open(f'{folder_path}/color_cache.csv', 'r', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for i in reader:
            current_color = i[0]

    # Получаем цвет от пользователя в команде /change_bg_color
    # При использовании команды с клавиатуры передаются параметры по умолчанию
    # (0, 0, 0) - для фона
    deligated_color = update.message.text.split()[1::]

    # Делаем проверку на существование аргумента(ов) у команды
    if deligated_color:
        # Проверяем, записан ли переданный цвет в шестнадцатеричной системе или в системе RGB
        if len(deligated_color[0]) < 6 or (len(deligated_color[0]) == 7 and deligated_color[0][0] == '#'):
            for i in range(len(deligated_color)):
                # Проверяем, есть ли в строках запятая, убираем при необходимости
                if ',' in deligated_color[i]:
                    deligated_color[i] = int(deligated_color[i][:-1:])
            deligated_color = tuple(deligated_color)
        elif len(deligated_color[0]) == 3 and len(deligated_color[1]) == 3 and len(deligated_color[2]) == 3:
            deligated_color = deligated_color[0]
        else:
            await update.message.reply_text('Упс, вы ввели цвет в нечитаемом для меня формате!')
            return
    else:
        await update.message.reply_text('Упс, вы ввели цвет в нечитаемом для меня формате!')
        return

    # Изменяем цвет фона и перезаписываем файл
    os.remove(f'{folder_path}/color_cache.csv')
    with open(f'{folder_path}/color_cache.csv', 'w', newline='', encoding='utf8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([current_color, deligated_color])
    reply_keyboard = [['/enter_text DeathMetalFan']]
    update.message.reply_text('Теперь введите текст:',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


async def change_text(update, context):  # Функция по изменения цвета текста
    user = update.effective_user
    folder_path = os.path.join(os.getcwd(), 'usercache', user.username)

    # Открываем файл в формате read и берём цвет фона
    with open(f'{folder_path}/color_cache.csv', 'r', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for i in reader:
            current_color = i[1]

        # Получаем цвет от пользователя в команде /change_text_color
        # При использовании команды с клавиатуры передаются параметры по умолчанию
        # (255, 255, 255) - для текста
        deligated_color = update.message.text.split()[1::]

        # Делаем проверку на существование аргумента(ов) у команды
        if deligated_color:
            # Проверяем, записан ли переданный цвет в шестнадцатеричной системе или в системе RGB
            if len(deligated_color[0]) < 6 or (len(deligated_color[0]) == 7 and deligated_color[0][0] == '#'):
                for i in range(len(deligated_color)):
                    # Проверяем, есть ли в строках запятая, убираем при необходимости
                    if ',' in deligated_color[i]:
                        deligated_color[i] = int(deligated_color[i][:-1:])
                deligated_color = tuple(deligated_color)
            elif len(deligated_color[0]) == 3 and len(deligated_color[1]) == 3 and len(deligated_color[2]) == 3:
                deligated_color = deligated_color[0]
            else:
                await update.message.reply_text('Упс, вы ввели цвет в нечитаемом для меня формате!')
                return
        else:
            await update.message.reply_text('Упс, вы ввели цвет в нечитаемом для меня формате!')
            return

    # Изменяем цвет текста и перезаписываем файл
    os.remove(f'{folder_path}/color_cache.csv')
    with open(f'{folder_path}/color_cache.csv', 'w', newline='', encoding='utf8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([deligated_color, current_color])
    reply_keyboard = [['/enter_text DeathMetalFan']]
    update.message.reply_text('Теперь введите текст:',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


async def enter_text(update, context):
    user = update.effective_user
    folder_path = os.path.join(os.getcwd(), 'usercache', user.username)
    text = ' '.join(update.message.text.split()[1::])

    # Открываем файл пользователя в формате read
    with open(f'{folder_path}/color_cache.csv', 'r', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for i in reader:
            color_text = i[0]
            color_bg = i[1]

    # Генерируем изображение
    generate(text, choice(os.listdir(f'static{os.sep}fonts{os.sep}')), user.username, )
    chat_id = user.id
    context.bot.send_photo(chat_id=chat_id, photo=open('tests/test.png', 'rb'))


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

    # Регистрируем обработчик в приложении.
    bot.add_handler(CommandHandler('start', start_function))
    bot.add_handler(CommandHandler('help', help_function))
    bot.add_handler(CommandHandler('img_gen', img_generator))
    bot.add_handler(CommandHandler('change_bg_color', change_bg))
    bot.add_handler(CommandHandler('change_text_color', change_text))
    bot.add_handler(CommandHandler('enter_text', enter_text))

    # Запускаем приложение.
    bot.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()

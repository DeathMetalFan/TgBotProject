import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime


def generate(line, font_name, username, bg_color=(0, 0, 0), txt_color=(255, 255, 255)):
    # Принимаем на вход текст, имя шрифта, цвета задника и текста

    IMG_WIDTH = 800

    # Создаем заготовку для вычисления размеров текста с применённым шрифтом
    font_image = Image.new("RGB", (100, 100), (0, 0, 0))

    # Загружаем шрифт
    font = ImageFont.truetype(f'static{os.sep}fonts{os.sep}{font_name}', 100)

    # Создаем инструмент для рисования на изображении
    font_draw = ImageDraw.Draw(font_image)

    # Получаем размеры текста
    text_width, text_height = font_draw.textsize(line, font)

    # Проверяем line на длину, если больше максимально допустимой ширины - разбиваем на несколько строк
    if text_width + 100 >= IMG_WIDTH:
        lines = []
        current_line = ''
        for i in line:
            if font_draw.textsize(current_line, font)[0] + 100 <= IMG_WIDTH:
                current_line += i
            else:
                # Переводим начальный и конечный символы строки в верхний регистр, остальные - в нижний
                list_of_letters = [i for i in current_line]
                list_of_letters[0] = list_of_letters[0].upper()
                list_of_letters[1:-1:] = [i.lower() for i in list_of_letters[1:-1:]]
                list_of_letters[-1] = list_of_letters[-1].upper()
                current_line = ''.join(list_of_letters)
                lines.append(current_line)
                current_line = ''
    else:
        lines = [line]

    # Заменяем text_width на максимальную длину строки из lines
    text_width = font_draw.textsize(max(lines, key=lambda x: len(x)), font)[0]

    # Создаём окончательное изображение
    text_width_height_tuple = int(text_width + 100), int(len(lines) * text_height * 0.7 + 50)
    current_image = Image.new("RGB", text_width_height_tuple, bg_color)
    draw = ImageDraw.Draw(current_image)

    # Отрисовываем каждую строку
    count = 0
    for i in lines:
        x = (current_image.width - font_draw.textsize(i, font)[0]) / 2
        y = int(text_height * count * 0.65)
        draw.text((x, y), i, txt_color, font=font)
        count += 1

    # Сохраняем изображение в папке пользователя
    current_image.save(f"usercache{os.sep}{username}{os.sep}{datetime.now()}.png")
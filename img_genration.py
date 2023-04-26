import os
from PIL import Image, ImageDraw, ImageFont


def generate(line, font_name, bg_color=(0, 0, 0), txt_color=(255, 255, 255)):
    # Принимаем на вход текст, имя шрифта, цвета задника и текста

    IMG_WIDTH = 800

    # Создаем заготовку для вычисления размеров текста с применённым шрифтом
    font_image = Image.new("RGB", (100, 100), (0, 0, 0))

    # Загружаем шрифт
    a = f'static{os.sep}fonts{os.sep}{font_name}'
    font = ImageFont.truetype(a, 100)

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
                lines.append(current_line)
                current_line = ''
    else:
        lines = [line]

    text_width = font_draw.textsize(max(lines, key=lambda x: len(x)), font)[0]

    # Создаём окончательное изображение
    text_width_height_tuple = text_width + 100, len(lines) * text_height + 50
    current_image = Image.new("RGB", text_width_height_tuple, bg_color)
    draw = ImageDraw.Draw(current_image)

    # Отрисовываем каждую строку
    count = 0
    for i in lines:
        x = (current_image.width - font_draw.textsize(i, font)[0]) / 2
        y = (text_height * count)
        draw.text((x, y), i, txt_color, font=font)
        count += 1

    # Сохраняем изображение
    current_image.save("logo.png")


generate('XavlegbmaofffassssitimiwoamndutroabcwapwaeiippohfffX'.upper(), 'maskdown.otf')
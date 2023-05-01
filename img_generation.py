import os
from PIL import Image, ImageDraw, ImageFont
from random import choice


def generate(line, txt_color=(255, 255, 255), bg_color=(0, 0, 0)):
    # Принимаем на вход текст, имя шрифта, цвета задника и текста

    IMG_WIDTH = 1000

    # Создаем заготовку для вычисления размеров текста с применённым шрифтом
    font_image = Image.new("RGB", (100, 100), (0, 0, 0))

    # Загружаем рандомный шрифт
    font_name = choice(os.listdir(f'static{os.sep}fonts{os.sep}'))
    font = ImageFont.truetype(f'static{os.sep}fonts{os.sep}{font_name}', 100)

    # Создаем инструмент для рисования на изображении
    font_draw = ImageDraw.Draw(font_image)

    # Если line - одно длинное слово
    if len(line.split()) == 1:
        # Получаем размеры текста
        text_width = font_draw.textsize(line, font)[0]

        # Проверяем line на длину, если больше максимально допустимой ширины - разбиваем на несколько строк
        if text_width + 100 >= IMG_WIDTH:
            lines = []
            current_line = []
            count = 0
            while len(' '.join(lines)) != len(' '.join(line)):
                # Создаём временный список с добавленным i
                a = current_line.copy()
                a.append(line[count])
                # Если временный список не превышает длиной максимальную ширину пикчи то добавляем i в основной
                if font_draw.textsize(' '.join(a), font)[0] < IMG_WIDTH:
                    current_line.append(line[count])
                    count += 1
                else:
                    lines.append(' '.join(current_line))
                    current_line = []
                if count == len(line):
                    lines.append(' '.join(current_line))
                    break

        else:
            lines = [line]
        # Первый и последний символы в каждой строке переводим в верхний регистр
        for i in range(len(lines)):
            # Первый и последний символы переводим в верхний регистр
            list_of_letters = [_ for _ in lines[i]]
            list_of_letters[0] = list_of_letters[0].upper()
            list_of_letters[1:-1:] = [i for i in list_of_letters[1:-1:]]
            list_of_letters[-1] = list_of_letters[-1].upper()
            lines[i] = ''.join(list_of_letters)

    # Если line - несколько слов
    else:
        line = line.split()
        for i in range(len(line)):
            # Первый и последний символы переводим в верхний регистр
            list_of_letters = [_ for _ in line[i]]
            list_of_letters[0] = list_of_letters[0].upper()
            list_of_letters[1:-1:] = [i.lower() for i in list_of_letters[1:-1:]]
            list_of_letters[-1] = list_of_letters[-1].upper()
            line[i] = ''.join(list_of_letters)
        if font_draw.textsize(' '.join(line), font)[0] > IMG_WIDTH:
            lines = []
            current_line = []
            count = 0
            while len(' '.join(lines)) != len(' '.join(line)):
                # Создаём временный список с добавленным i
                a = current_line.copy()
                a.append(line[count])
                # Если временный список не превышает длиной максимальную ширину пикчи то добавляем i в основной
                if font_draw.textsize(' '.join(a), font)[0] < IMG_WIDTH:
                    current_line.append(line[count])
                    count += 1
                else:
                    lines.append(' '.join(current_line))
                    current_line = []
                if count == len(line):
                    lines.append(' '.join(current_line))
                    break
        else:
            lines = []
            lines.append(' '.join(line))

    # Получаем размеры изображения
    text_width, text_height = font_draw.textsize(max(lines, key=lambda x: len(x)), font)

    # Создаём окончательное изображение
    text_width_height_tuple = int(text_width + 100), int(len(lines) * text_height * 0.7 + 100)
    current_image = Image.new("RGB", text_width_height_tuple, bg_color)
    draw = ImageDraw.Draw(current_image)

    # Отрисовываем каждую строку
    count = 0
    for i in lines:
        x = (current_image.width - font_draw.textsize(i, font)[0]) / 2
        y = int(text_height * count * 0.8)
        draw.text((x, y), i, txt_color, font=font)
        count += 1

    # Делегируем изображение в main
    return current_image
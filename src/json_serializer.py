import json
import os

# Функция для инициализации файла
def init_json_file(filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('[')  # Начало массива JSON

# Функция для добавления пользователя в файл
def add_user_to_json(filename, user_data):
    with open(filename, 'a', encoding='utf-8') as f:
        # Проверяем, если файл содержит только начальный символ, добавляем объект
        if os.stat(filename).st_size == 1:  # Файл только с '['
            json.dump(user_data, f, ensure_ascii=False, indent=4)
        else:
            f.write(',\n')  # Запятая перед новой записью
            json.dump(user_data, f, ensure_ascii=False, indent=4)

# Функция для завершения записи
def close_json_file(filename):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(']')  # Закрываем массив JSON с новой строки для формата
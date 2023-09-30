#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import tkinter as tk
from tkinter import filedialog
from tkinter import Scrollbar

# Создаем главное окно
root = tk.Tk()
root.title("Отображение значений из файла")

# Создаем текстовое поле для вывода значений
text_widget = tk.Text(root, height=40, width=160)
text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Добавляем полосу прокрутки
scrollbar = Scrollbar(root, command=text_widget.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_widget.config(yscrollcommand=scrollbar.set)

# Устанавливаем значение по умолчанию для category
category = "language_window"
parsed_data = {}  # Словарь для хранения данных после разбора файла
parsed_data["comments"] = []
parsed_data[category] = {}

def widget_clear():
    text_widget.delete(1.0, tk.END)  # Очищаем текстовое поле

def widget_print(data, index = tk.END):
    text_widget.insert(index, data)  # Выводим Категорию, Ключ, Значение

def is_ignore_line(line):
    global parsed_data
    # Пропускаем разделители — пустые строки
    if not line:
        return True
    # Игнорируем комментарии
    if line.startswith("//"):
        parsed_data["comments"].append(line[len("// "):])
        return True
    return False

# Функция для открытия файла через диалоговое окно
def open_file_dialog():
    global category, parsed_data  # Сделаем category и parsed_data глобальными переменными
    file_types = [
        ("Text Files (Tixati Language)", "*.txt"),
        ("Json File", "*.json"),
        ("All Files", "*.*")
    ]
    path = filedialog.askopenfilename(filetypes=file_types)
    if not path:
        return
    filename = path.split('/')[len(path.split('/'))-1]
    widget_clear()
    widget_print(f"File \"{filename}\" content:\n")
    if path.endswith(".json"):
        with open(path, 'r') as file:
            parsed_data = json.load(file)
        widget_print(json.dumps(parsed_data, indent=2)) # Выводим Категорию, Ключ, Значение
    else:
        with open(path, "r") as file:
            lines = file.readlines()
        parse_txt_file(lines)  # Вызываем функцию для разбора файла

# Функция для разбора файла и вывода данных
def parse_txt_file(lines):
    global category, parsed_data  # Сделаем category и parsed_data глобальными переменными
    line_num = -1
    for line in lines:
        line_num += 1
        line = line.strip()
        if line.startswith("///////"):
            widget_print(f"{json.dumps({category: parsed_data[category]}, indent=2)},\n")
            category = line[len("/////// "):]  # Удаляем "/////// " из начала строки
            if not category in parsed_data:
                parsed_data[category] = {}
            continue
        if is_ignore_line(line):
            continue
        key = line
        value = lines.pop(line_num + 1).strip()  # Получаем следующую строку (Значение)
        parsed_data[category][key] = value  # Добавляем данные в список

# Кнопка для выбора файла через диалоговое окно
open_button = tk.Button(root, text="Выбрать файл", command=open_file_dialog)
open_button.pack()

# Функция для сохранения данных в JSON файл
def save_json(data):
    file_types = [("JSON Files", "*.json"), ("All Files", "*.*")]
    path = filedialog.asksaveasfilename(filetypes=file_types, defaultextension=".json")
    if path:
        with open(path, "w") as json_file:
            json.dump(data, json_file, indent=2)
        print(f"Данные сохранены в файл: {path}")

# Кнопка для сохранения JSON файла
save_button = tk.Button(root, text="Сохранить JSON", command=lambda: save_json(parsed_data))
save_button.pack()

# Запускаем главный цикл приложения
root.mainloop()
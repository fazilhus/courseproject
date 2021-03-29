# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 04:02:39 2021

@author: khusn
"""

import tkinter as tk
import os
import time as t
import cchardet
import hashlib

file_path = ''   

# Функция отвечающая за непосредственно архивирование выбранного файла
def encode_lz78(s):
    buffer = ''
    dictionary = {}
    ans = []
    length = 0
    progress_bar['maximum'] = len(s)
    time = t.time()
    for i in range(len(s)):
        if t.time() - time > 0.05:
            time = t.time()
            progress_bar['value'] += i
            root.update()
        if (buffer + s[i]) in dictionary.keys():
            buffer += s[i]
        else:
            if dictionary.get(buffer) is None:
                ans.append((0, s[i]))
            else:
                ans.append((dictionary.get(buffer), s[i]))
            length += 1
            dictionary.update({buffer + s[i]: length})
            buffer = ''
    if not (buffer == ''):
        last_char = buffer[-1]
        buffer = buffer[:-1]
        if dictionary.get(buffer) is None:
            ans.append((0, last_char))
        else:
            ans.append((dictionary.get(buffer), last_char))
    return ans

# Функция отвечающая за непосредственно разархивирование выбранного файла
def decode_lz78(inp):
    s = inp[1:-1].split(')(')
    encoded = []
    for i in range(len(s)):
        pos = s[i].find(',')
        encoded.append([int(s[i][:pos]), s[i][pos + 1:]])
    lst = ['']
    ans = ''
    progress_bar['maximum'] = len(encoded)
    time = t.time()
    for i in range(len(encoded)):
        if t.time() - time > 0.05:
            time = t.time()
            progress_bar['value'] += i
            root.update()
        node = encoded[i]
        word = lst[node[0]] + node[1]
        ans += word
        lst.append(word)
    return ans


# Функция, вызываемя при срабатывании кнопки "Открыть". Сохраняет путь к файлу в глобальной переменной.
def open_file():
    global file_path

    file_path = tk.filedialog.askopenfilename(initialdir='/', title='Выберите файл',
                                           filetypes=(('Text files', '*.txt'), ('LZ78 Archives', '*.lz78'),
                                                      ('All files', '*.*')))
    path_result = tk.StringVar(root)
    file_path_label['textvariable'] = path_result
    path_result.set(file_path)
    if os.path.splitext(file_path)[1] == '.txt':
        archive['state'] = 'normal'
        dearchive['state'] = 'disabled'
    elif os.path.splitext(file_path)[1] == '.lz78':
        archive['state'] = 'disabled'
        dearchive['state'] = 'normal'

# Функция, вызываемя при срабатывании кнопки "Архивировать". Вызывает функцию encode_lz78, создает новый файл с прежним названием с новым расширением.
def encode():
    global file_path

    new_file_path = tk.filedialog.asksaveasfilename(initialdir='/', title='Назовите файл')

    is_pwd = tk.messagebox.askquestion(title='Пароль', message='Установить пароль?')
    '''if is_pwd == 'yes':
        pwd = tk.Entry(root,show='*').get()'''

    with open(file_path, 'rb') as f:
        encoding = cchardet.detect(f.read())['encoding']

    f = open(file_path, 'r', encoding=encoding)
    s = f.read()
    ans1 = encode_lz78(s)
    f.close()

    file_path = new_file_path[:-5] + '.lz78'
    f = open(file_path, 'w', encoding=encoding)
    for i in range(len(ans1)):
        f.write('(' + str(ans1[i][0]) + ',' + ans1[i][1] + ')')
    f.close()

    path_result = tk.StringVar(root)
    file_path_label['textvariable'] = path_result
    path_result.set(file_path)

    archive['state'] = 'disabled'
    progress_bar['value'] = 0.0

# Функция, вызываемя при срабатывании кнопки "Разархивировать". Вызывает функцию decode_lz78, создает новый файл с прежним названием с расширением .txt.
def decode():
    global file_path
    
    new_file_path = tk.filedialog.asksaveasfilename(initialdir='/', title='Назовите файл')

    with open(file_path, 'rb') as f:
        encoding = cchardet.detect(f.read())['encoding']

    f = open(file_path, 'r', encoding=encoding)
    ans2 = decode_lz78(f.read())
    f.close()

    file_path = new_file_path[:-4] + '.txt'
    f = open(file_path, 'w', encoding=encoding)
    f.write(ans2)
    f.close()

    path_result = tk.StringVar(root)
    file_path_label['textvariable'] = path_result
    path_result.set(file_path)

    dearchive['state'] = 'disabled'
    progress_bar['value'] = 0.0

# Инициализация главного окна приложения
root = tk.Tk()
root.title('Архиватор')
root.resizable(0, 0)

content = tk.Frame(root, bg="white")

frame0 = tk.Frame(content, height=10, width=1, bg='white')
frame11 = tk.Frame(content, height=1, width=30, bg='white')
frame12 = tk.Frame(content, height=1, width=60, bg='white')
frame13 = tk.Frame(content, height=1, width=30, bg='white')
frame2 = tk.Frame(content, height=60, width=1, bg='white')
frame6 = tk.Frame(content, height=10, width=1, bg='white')
frame8 = tk.Frame(content, height=10, width=1, bg='white')

# Объявление элементов интерфейса
label = tk.Label(content, width=32, fg='black', bg='white', text='Путь к файлу:')
file_path_label = tk.Label(content, width=96, fg='black', bg='lightgrey')  # Надпись пути к файлу
open_file = tk.Button(content, height=1, width=12, text='Выбрать файл', padx=10, pady=5, fg='black', bg='white',  # Кнопка "Выбрать файл"
                     activebackground='grey', justify='center', default='active', command=open_file)
archive = tk.Button(content, height=1, width=12, text='Архивировать', padx=10, pady=5, fg='black', bg='white',  # Кнопка "Архивировать"
                    activebackground='grey', justify='center', state='disabled', command=encode)
dearchive = tk.Button(content, height=1, width=12, text='Разархивировать', padx=10, pady=5, fg='black', bg='white',  # Кнопка "Разархивировать"
                      activebackground='grey', justify='center', state='disabled', command=decode)
progress_bar_label = tk.Label(content, width=32, fg='black', bg='white', text='Прогресс:')
password_entry = tk.Entry()
progress_bar = tk.ttk.Progressbar(content, length=500, mode='determinate')  # Прогрессбар

# Сетка, по которой размещаются объекты интерфейса
content.grid(column=0, row=0)
frame0.grid(column=0, row=0)
label.grid(column=1, row=2)
frame11.grid(column=0, row=3)
file_path_label.grid(column=1, row=3)
frame12.grid(column=2, row=3)
open_file.grid(column=3, row=3)
frame13.grid(column=4, row=3)
frame2.grid(column=0, row=4)
progress_bar_label.grid(column=1, row=5)
progress_bar.grid(column=1, row=7)
archive.grid(column=3, row=5)
frame6.grid(column=0, row=6)
dearchive.grid(column=3, row=7)
frame8.grid(column=0, row=8)

root.mainloop()

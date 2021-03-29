import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import time as t
import cchardet

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
        if t.time() - time > 0.03:
            time = t.time()
            progress_bar['value'] = i
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
    encoded = []
    for i in range(inp.find('|'), len(inp)):
        if inp[i] == '|' and inp[i - 1] != ',':
            encoded.append(inp[i - 3:i].split(','))
    encoded.append(inp[inp.rfind('|') + 1:].split(','))
    dictionary = ['']
    ans = ''
    progress_bar['maximum'] = len(encoded)
    time = t.time()
    for i in range(len(encoded)):
        if t.time() - time > 0.03:
            time = t.time()
            progress_bar['value'] = i
            root.update()
        node = encoded[i]
        word = dictionary[int(node[0])] + node[1]
        ans += word
        dictionary.append(word)
    return ans

# Функция, вызываемя при срабатывании кнопки "Открыть". Сохраняет путь к файлу в глобальной переменной.
def open_file():
    global file_path

    file_path = filedialog.askopenfilename(initialdir='/', title='Выберите файл',
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

    with open(file_path, 'rb') as f:
        encoding = cchardet.detect(f.read())['encoding']
        print(encoding)

    with open(file_path, 'r', encoding='utf-8') as f:
        ans1 = encode_lz78(f.read())

    file_path = os.path.splitext(file_path)[0] + '.lz78'
    with open(file_path, 'w', encoding='utf-8') as f:
        for elem in ans1[:-1]:
            f.write(str(elem[0]) + ',' + elem[1] + '|')
        f.write(str(ans1[-1][0]) + ',' + ans1[-1][1])

    path_result = tk.StringVar(root)
    file_path_label['textvariable'] = path_result
    path_result.set(file_path)

    archive['state'] = 'disabled'
    progress_bar['value'] = 0.0

# Функция, вызываемя при срабатывании кнопки "Разархивировать". Вызывает функцию decode_lz78, создает новый файл с прежним названием с расширением .txt.
def decode():
    global file_path

    '''with open(file_path, 'rb') as f:
        encoding = cchardet.detect(f.read())['encoding']
        print(encoding)'''

    with open(file_path, 'r', encoding='utf-8') as f:
        ans2 = decode_lz78(f.read())

    file_path = os.path.splitext(file_path)[0] + '.txt'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(ans2)

    path_result = tk.StringVar(root)
    file_path_label['textvariable'] = path_result
    path_result.set(file_path)

    dearchive['state'] = 'disabled'
    progress_bar['value'] = 0.0

# Инициализация окна приложения
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
progress_bar = ttk.Progressbar(content, length=500, mode='determinate')  # Прогрессбар

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

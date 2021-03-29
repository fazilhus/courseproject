#---IMPORTS---

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import time as t
import cchardet


#---FUNCTIONS---

# Функция отвечающая за непосредственно архивирование выбранного файла
def EncodeLZ78(s):
    buffer = ''
    dictionary = {}
    ans = []
    length = 0
    progressBar['maximum'] = len(s)
    time = t.time()
    for i in range(len(s)):
        if t.time() - time > 0.05:
            time = t.time()
            progressBar['value'] += i
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
        lastChar = buffer[-1]
        buffer = buffer[:-1]
        if dictionary.get(buffer) is None:
            ans.append((0, lastChar))
        else:
            ans.append((dictionary.get(buffer), lastChar))
    return ans

# Функция отвечающая за непосредственно разархивирование выбранного файла
def DecodeLZ78(inp):
    s = inp[1:-1].split(')(')
    encoded = []
    for i in range(len(s)):
        pos = s[i].find(',')
        encoded.append([int(s[i][:pos]), s[i][pos + 1:]])
    dictionary = ['']
    ans = ''
    progressBar['maximum'] = len(encoded)
    time = t.time()
    for i in range(len(encoded)):
        if t.time() - time > 0.05:
            time = t.time()
            progressBar['value'] += i
            root.update()
        node = encoded[i]
        word = dictionary[node[0]] + node[1]
        ans += word
        dictionary.append(word)
    return ans

# Функция, вызываемя при срабатывании кнопки "Открыть". Сохраняет путь к файлу в глобальной переменной.
def OpenFile():
    global filePath

    filePath = filedialog.askopenfilename(initialdir='/', title='Выберите файл',
                                          filetypes=(('Text files', '*.txt'), ('LZ78 Archives', '*.lz78'), ('All files', '*.*')))
    pathResult = tk.StringVar(root)
    filePathLabel['textvariable'] = pathResult
    pathResult.set(filePath)
    if '.txt' in filePath:
        archive['state'] = 'normal'
        deArchive['state'] = 'disabled'
    elif '.lz78' in filePath:
        archive['state'] = 'disabled'
        deArchive['state'] = 'normal'

# Функция, вызываемя при срабатывании кнопки "Архивировать". Вызывает функцию
def Archive():
    global filePath

    with open(filePath, 'rb') as f:
        encoding = cchardet.detect(f.read())['encoding']
        print(encoding)

    f = open(filePath, 'r', encoding=encoding)
    s = f.read()
    ans1 = EncodeLZ78(s)
    f.close()

    filePath = filePath[:-4] + '.lz78'
    f = open(filePath, 'w', encoding=encoding)
    for i in range(len(ans1)):
        f.write('(' + str(ans1[i][0]) + ',' + ans1[i][1] + ')')
    f.close()

    pathResult = tk.StringVar(root)
    filePathLabel['textvariable'] = pathResult
    pathResult.set(filePath)

    archive['state'] = 'disabled'
    progressBar['value'] = 0.0

#
def DeArchive():
    global filePath

    with open(filePath, 'rb') as f:
        encoding = cchardet.detect(f.read())['encoding']
        print(encoding)

    f = open(filePath, 'r', encoding=encoding)
    ans2 = DecodeLZ78(f.read())
    f.close()

    filePath = filePath[:-5] + '.txt'
    f = open(filePath, 'w', encoding=encoding)
    f.write(ans2)
    f.close()

    pathResult = tk.StringVar(root)
    filePathLabel['textvariable'] = pathResult
    pathResult.set(filePath)

    deArchive['state'] = 'disabled'
    progressBar['value'] = 0.0


#---INIT---


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

label = tk.Label(content, width=32, fg='black', bg='white', text='Путь к файлу:')
filePathLabel = tk.Label(content, width=96, fg='black', bg='lightgrey')
openFile = tk.Button(content, height=1, width=12, text='Открыть', padx=10, pady=5, fg='black', bg='white',
                     activebackground='grey', justify='center', default='active', command=OpenFile)
archive = tk.Button(content, height=1, width=12, text='Архивировать', padx=10, pady=5, fg='black', bg='white',
                    activebackground='grey', justify='center', state='disabled', command=Archive)
deArchive = tk.Button(content, height=1, width=12, text='Разархивировать', padx=10, pady=5, fg='black', bg='white',
                      activebackground='grey', justify='center', state='disabled', command=DeArchive)
progressBarLabel = tk.Label(content, width=32, fg='black', bg='white', text='Прогресс:')
progressBar = ttk.Progressbar(content, length=600, mode='determinate')


#---GRID---

content.grid(column=0, row=0)
frame0.grid(column=0, row=0)
label.grid(column=1, row=2)
frame11.grid(column=0, row=3)
filePathLabel.grid(column=1, row=3)
frame12.grid(column=2, row=3)
openFile.grid(column=3, row=3)
frame13.grid(column=4, row=3)
frame2.grid(column=0, row=4)
progressBarLabel.grid(column=1, row=5)
progressBar.grid(column=1, row=7)
archive.grid(column=3, row=5)
frame6.grid(column=0, row=6)
deArchive.grid(column=3, row=7)
frame8.grid(column=0, row=8)


root.mainloop()
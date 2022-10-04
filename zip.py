import shutil
from cryptography.fernet import Fernet
import os
from tkinter import Tk, Label, Button
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

print('''

████─█──█─███─████─███─████
█──█─██─█─█─────██──█──█──█
█──█─█─██─███──██───█──████
█──█─█──█─█───██────█──█
████─█──█─███─████─███─█

''')

while True:
    def copy_to_clipboard():
        root.clipboard_clear()  # Очистить буфер обмена
        root.clipboard_append(lbl['text'])  # Добавить текст в буфер обмена
    def KeyGet():
        while True:
            key = input('')
            try:
                global f
                f = Fernet(key)
                break
            except:
                print('Неверный ключ, попробуйте снова')
                continue

    print('Выберите объект для работы: Файл [1] | Архив [2] | Выход [0]')
    a = int(input())

    if a == 1:
        print('''Выберите задачу: Шифровка [1] | Расшифровка [2]''')
        choice = int(input(''))

        if choice == 1:
            #Создание ключа
            print('Создание ключа шифрования...')
            key = Fernet.generate_key()
            str(key)
            key = key.decode('utf-8')
            root = Tk()
            root.title("Сохраните ключ")   
            lbl = Label(root, text=key)
            btn = Button(root, text='copy', command=copy_to_clipboard)
            lbl.grid(row=0, column=0)
            btn.grid(row=1, column=0)
            w, h = 365, 55
            root.geometry(f"{w}x{h}+{(root.winfo_screenwidth()-w)//2}+{(root.winfo_screenheight()-h)//2}")
            root.mainloop()
            f = Fernet(key)
            #Выбор файла
            Tk().withdraw()
            file = askopenfilename()
            #Сохранение имени и расщирения файла
            try:
                with open(file, 'rb') as original_file:
                    original = original_file.read()
            except:
                break
            #Шифрование файла
            encrypted = f.encrypt(original)
            print('Куда сохранить файл?')
            Tk().withdraw()
            path_to_save_file = askdirectory()
            print('Кодирование...')
            name = path_to_save_file + '/enc_' + os.path.basename(file)
            print(name)
            with open(name, 'wb') as encrypted_file:
                encrypted_file.write(encrypted)
            encrypted_file_path = os.path.abspath(name)

            print('Файл закодирован')
            continue

        if choice == 2:
            #Получение ключа
            print('Введите ключ шифрования:')
            KeyGet()
            #Получение файла
            print('Выберите файл для расшифровки')
            file_enc = askopenfilename()
            try:
                with open(file_enc, 'rb') as encrypted_file:
                    encrypted = encrypted_file.read()
            except:
                break
            print('Куда сохранить файл?')
            Tk().withdraw()
            path_to_save_file = askdirectory()

            decrypted = f.decrypt(encrypted)
            name = 'path_to_save_file' + '/dec_' + os.path.basename(file_enc)
            with open(name, 'wb') as decrypted_file:
                decrypted_file.write(decrypted)
            decrypted_file_path = os.path.abspath(name)
            #Место сохранения файла
            print('Куда сохранить файл?')
            Tk().withdraw()
            path_to_save_file = askdirectory()
            shutil.move(decrypted_file_path, path_to_save_file)

            print('Файл Расшифрован')
            continue

    if a == 2:

        print('''Выберите задачу: Создание архива [1] | Извлечение архива [2] | Создание архива с шифрованием [3] | Извлечение зашифрованного архива [4]''')

        choice = int(input())

        #Архивация
        if choice == 1:
            Tk().withdraw()
            path_to_zip_folder = askdirectory()
            name = input('Как назвать архив? > ')
            #Выбор формата архива
            type_list = ['zip', 'tar', 'gztar']
            type_of_archive = int(input('В каком формате создать архив? zip[0] | tar[1] | gztar [2] > '))
            print('Создание архива...')
            shutil.make_archive(name, type_list[type_of_archive], path_to_zip_folder)
            archive_file_path = os.path.abspath(name+'.'+type_list[type_of_archive])
            #Место сохранения файла
            print('Куда сохранить архив?')
            Tk().withdraw()
            path_to_save_archive = askdirectory()
            shutil.move(archive_file_path, path_to_save_archive)
            print('Архив создан✅')
            continue

        #Распаковка
        if choice == 2:
            print('Выберите папку для Архивации')
            path_to_archive = askopenfilename()
            print('Где распаковать?')
            path_to_extract = askdirectory()
            print('Распаковка...')
            shutil.unpack_archive(path_to_archive, path_to_extract)
            print('Архив распакован✅')
            continue

        #Архивация с шифрованием
        if choice == 3:
            path_to_zip_folder = askdirectory()
            name = input('Как назвать архив? > ')
            #Выбор формата архива
            type_list = ['zip', 'tar', 'gztar']
            type_of_archive = int(input('В каком формате создать архив? zip[0] | tar[1] | gztar [2] > '))
            print('Создание архива...')
            shutil.make_archive(name, type_list[type_of_archive], path_to_zip_folder)
            print('Архив создан✅')
            #Создание ключа
            print('Создание ключа шифрования...')
            key = Fernet.generate_key()
            str(key)
            key = key.decode('utf-8')
            root = Tk()
            root.title("Сохраните ключ")   
            lbl = Label(root, text=key)
            btn = Button(root, text='copy', command=copy_to_clipboard)
            lbl.grid(row=0, column=0)
            btn.grid(row=1, column=0)
            w, h = 365, 55
            root.geometry(f"{w}x{h}+{(root.winfo_screenwidth()-w)//2}+{(root.winfo_screenheight()-h)//2}")
            f = Fernet(key)
            file = name + '.' + str(type_list[type_of_archive])

            name, ext = os.path.splitext(file)
            with open(file, 'rb') as original_file:
                original = original_file.read()
            #Шифрование файла
            encrypted = f.encrypt(original)
            print('Кодирование...')
            #Установка начатьного имени файла
            name = 'enc_' + name + ext
            with open(name, 'wb') as encrypted_file:
                encrypted_file.write(encrypted)
            print('Архив закодирован')
            os.remove(file)
            continue

        #Распаковка + расшифровка
        if choice == 4:
            #Получение ключа
            print('Введите ключ шифрования:')
            key = input('')
            KeyGet()
            #Получение файла
            print('Выберите файл для расшифровки')
            file_enc = askopenfilename()
            try:
                with open(file_enc, 'rb') as encrypted_file:
                    encrypted = encrypted_file.read()
            except:
                break
            decrypted = f.decrypt(encrypted)
            with open(file_enc, 'wb') as decrypted_file:
                decrypted_file.write(decrypted)                    
            print('Файл Расшифрован')
            continue
    else:
        break

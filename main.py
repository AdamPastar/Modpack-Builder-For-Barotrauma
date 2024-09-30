import os
import sys
import xml.etree.ElementTree as ET
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# Создание основного окна приложения
def create_gui():
    # Основное окно
    window = tk.Tk()
    window.title("Modpack Builder For Barotrauma")
    window.geometry("400x50")

    # Запрет на изменение размера окна
    window.resizable(False, False)

    # Включаем тёмную тему для окна
    window.configure(bg='#2e2e2e')

    # Фрейм для кнопок
    button_frame = tk.Frame(window, bg='#2e2e2e')
    button_frame.pack(pady=10)

    # Кнопка "Собрать пакет" с тёмной темой
    build_button = tk.Button(button_frame, text="Собрать пакет", command=lambda: build_pack(window), font=("Arial", 12), bg='#444444', fg='#ffffff')
    build_button.pack(side=tk.LEFT, padx=10)

    # Кнопка "Выйти" с тёмной темой
    exit_button = tk.Button(button_frame, text="Выйти", command=window.quit, font=("Arial", 12), bg='#444444', fg='#ffffff')
    exit_button.pack(side=tk.LEFT, padx=10)

    window.mainloop()

# Функция для выбора папки Barotrauma
def select_barotrauma_folder():
    folder_path = filedialog.askdirectory(title="Выберите папку Barotrauma <-----")
    if folder_path and os.path.isdir(os.path.join(folder_path, 'LocalMods')) and os.path.isdir(os.path.join(folder_path, 'ModLists')):
        return folder_path.replace('\\', '/')
    else:
        messagebox.showerror("Ошибка", "В выбранной папке должны находиться папки 'LocalMods' и 'ModLists'.")
        return None

# Функция для поиска папок
def find_folders(path):
    for item in os.listdir(path):
        if os.path.isfile(os.path.join(path, item)):
            continue
        else:
            yield item

# Основной функционал сборки пакетов модов
def build_pack(window):
    # Основной код
    main = select_barotrauma_folder()

    if main:
        print(f"Вы выбрали папку: {main}")
    else:
        print("Папка не выбрана!")
        return

    # Изменение заголовка во время сборки
    window.title("Сборка модов... ")

    # Создание нужных директорий
    try:
        os.mkdir(main + '/Making de pack')
        os.mkdir(main + '/You can delete it')
    except FileExistsError:
        pass

    # Путь к папке LocalMods
    mods_path = os.path.join(main, 'LocalMods')

    # Путь к файлу mods.xml
    xml_path = filedialog.askopenfilename(title="Выберите файл .xml из папки ModLists <-----", initialdir=os.path.join(main, 'ModLists'), filetypes=[("XML files", "*.xml")])
    if not xml_path:
        return

    # Извлечение имени XML-файла без расширения
    xml_filename = os.path.splitext(os.path.basename(xml_path))[0]

    os.chdir(mods_path)

    # Поиск и обработка папок
    for folder in find_folders(mods_path):
        try:
            root = ET.parse(os.path.join(main, 'LocalMods', folder, 'filelist.xml')).getroot()
            with open(os.path.join(main, 'You can delete it', root.attrib['name'] + '.txt'), 'w') as f:
                f.write(folder)
        except Exception as e:
            print(f"Ошибка обработки папки {folder}: {e}")

    # Чтение и копирование файлов из ModLists
    try:
        e = ET.parse(xml_path).getroot()

        for child in e.iter('Local'):
            with open(os.path.join(main, 'You can delete it', child.attrib['name'] + '.txt'), 'r') as f:
                get_id = f.read()

            source_dir = os.path.join(main, 'LocalMods', get_id + '/')
            destination_dir = os.path.join(main, 'Making de pack', get_id + '/')

            shutil.copytree(source_dir, destination_dir)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при чтении файла mods.xml: {e}")
        return

    # Создание директории bin, если её нет
    bin_dir = os.path.join(main, 'bin')
    os.makedirs(bin_dir, exist_ok=True)

    # Создание временной папки для архива
    temp_archive_dir = os.path.join(main, 'temp_archive')
    os.makedirs(temp_archive_dir, exist_ok=True)

    # Копируем содержимое из папки "Making de pack" во временную папку
    for item in os.listdir(os.path.join(main, 'Making de pack')):
        src_path = os.path.join(main, 'Making de pack', item)
        dst_path = os.path.join(temp_archive_dir, item)

        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)  # Используйте copytree для папок
        else:
            shutil.copy2(src_path, dst_path)  # Используйте copy2 для файлов

    # Создание ZIP-архива с именем XML-файла
    try:
        zip_path = shutil.make_archive(os.path.join(bin_dir, xml_filename), 'zip', temp_archive_dir)
        messagebox.showinfo("Успех", f"Пакет '{xml_filename}.zip' успешно собран и сохранён в папке 'bin'!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при создании архива: {e}")

    # Удаление временных папок
    shutil.rmtree(os.path.join(main, 'Making de pack'), ignore_errors=True)
    shutil.rmtree(os.path.join(main, 'You can delete it'), ignore_errors=True)
    shutil.rmtree(temp_archive_dir, ignore_errors=True)

    # Возвращаем заголовок обратно
    window.title("Конструктор пакетов модов")

if __name__ == "__main__":
    create_gui()

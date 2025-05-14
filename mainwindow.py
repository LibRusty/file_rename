from book import Book
from decompressor_factory import DecompressorFactory
from renamer import Renamer
from settings import Settings
from settingswindow import SettingsWindow
import os
import sys
import hashlib
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTreeView, QFileSystemModel, QVBoxLayout, QWidget, QLabel, 
    QLineEdit, QPushButton, QTextEdit, QHBoxLayout, QAction
)
from PyQt5.QtCore import Qt, QDir, QFileSystemWatcher
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow):
    def __init__(self, settings):
        super().__init__()
        self.decompressor_factory = DecompressorFactory()
        self.settings = settings
        self.renamer = Renamer(self.settings)
        self.watcher = QFileSystemWatcher()
        self.settings.add_observer(self)
        self.update_watched_folder()

        self.history = []  
        self.processed_files = self.load_processed_files()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setMinimumSize(640, 480)  
        self.resize(1600, 1000)

        self.init_menu()

        layout = QHBoxLayout(central_widget)

        # Левое окно: дерево каталогов
        self.dir_model = QFileSystemModel()
        self.dir_model.setFilter(QDir.NoDotAndDotDot |QDir.AllDirs | QDir.AllEntries)
        self.dir_model.setNameFilters(["*.epub", "*.fb2", "*.rtf", "*.pdf", "*.mobi", "*.fb3"]) 
        self.dir_model.setNameFilterDisables(False)

        app_directory = os.path.abspath(__file__)
        home_path = os.path.splitdrive(app_directory)[0]
        self.dir_model.setRootPath(home_path)

        self.file_tree = QTreeView()
        self.file_tree.setModel(self.dir_model)
        self.file_tree.setRootIndex(self.dir_model.index(home_path))
        self.file_tree.clicked.connect(self.on_tree_item_click)

        layout.addWidget(self.file_tree, 1)

        # Правая панель для отображения информации и управления
        right_panel = QVBoxLayout()

        # Информация о выбранном файле
        self.selected_file_label = QLabel("Имя файла: ")
        right_panel.addWidget(self.selected_file_label)

        # Поле для нового имени файла
        self.new_file_name_input = QLineEdit()
        right_panel.addWidget(QLabel("Новое имя файла:"))
        right_panel.addWidget(self.new_file_name_input)

        # Кнопка для переименования
        self.rename_button = QPushButton("Переименовать")
        self.rename_button.clicked.connect(self.rename_selected_file)
        right_panel.addWidget(self.rename_button)

        # Отображение названия книги
        self.file_name_text = QLineEdit()
        self.file_name_text.setReadOnly(True)
        right_panel.addWidget(QLabel("Название книги:"))
        right_panel.addWidget(self.file_name_text)

        # Отображение автора книги
        self.file_author_text = QLineEdit()
        self.file_author_text.setReadOnly(True)
        right_panel.addWidget(QLabel("Автор книги:"))
        right_panel.addWidget(self.file_author_text)

        # История операций
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        right_panel.addWidget(QLabel("История действий:"))
        right_panel.addWidget(self.history_text)

        layout.addLayout(right_panel, 2)

        self.setWindowTitle("File Renamer")
        self.setWindowIcon(QIcon("icon.ico")) 
        self.resize(800, 600)

    def load_processed_files(self):
        processed_files_path = 'processed_files.txt'
        if os.path.exists(processed_files_path):
            with open(processed_files_path, 'r') as file:
                return [line.strip() for line in file.readlines()]
        return []
    
    def save_processed_files(self):
        with open('processed_files.txt', 'w') as file:
            for file_name in self.processed_files:
                file.write(file_name + '\n')
    

    def init_menu(self):
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("Настройки")
        open_settings_action = QAction("Открыть Настройки", self)
        open_settings_action.triggered.connect(self.open_settings_window)
        settings_menu.addAction(open_settings_action)

    def open_settings_window(self):
        self.settings_window = SettingsWindow(self.settings, parent=self)
        self.settings_window.setWindowModality(Qt.ApplicationModal) 
        self.settings_window.show()
        

    def on_tree_item_click(self, index):
        self.file_name_text.clear()
        self.file_author_text.clear()
        self.file_path = self.dir_model.filePath(index)
        self.selected_file_label.setText(f"Имя файла: {self.file_path}")
        self.current_file = self.file_path

        if os.path.isfile(self.current_file):
            try:
                self.decompressor = self.decompressor_factory.get_decompressor(self.current_file)
                self.book = self.decompressor.decompress(self.current_file)
                self.new_file_name_input.setText(self.renamer.create_name(self.book))
                self.file_name_text.setText(self.book.get_name())
                self.file_author_text.setText(self.book.get_author())
            except FileNotFoundError as e:
                self.notify(f"Ошибка: {e} (файл повреждён или не является EPUB)")
            except Exception as e:
                self.notify(f"Неизвестная ошибка: {e}")


    def rename_selected_file(self):
        if not hasattr(self, 'current_file'):
            self.notify("Файл не выбран.")
            return

        new_name = self.new_file_name_input.text().strip()
        if not new_name:
            self.notify("Новое имя не может быть пустым.")
            return

        new_file_path = os.path.join(os.path.dirname(self.current_file), new_name) + os.path.splitext(self.file_path)[1]
        self.rename_file_logic(self.current_file, new_file_path)

    def move_selected_file(self):
        if not hasattr(self, 'current_file'):
            self.notify("Файл не выбран.")
            return

        new_folder = self.new_folder_input.text().strip()
        if not new_folder or not os.path.isdir(new_folder):
            self.notify("Указан неверный путь для новой папки.")
            return

        new_file_path = os.path.join(new_folder, os.path.basename(self.current_file))
        self.rename_file_logic(self.current_file, new_file_path)

    def rename_file_logic(self, old_name, new_name):
        try:
            os.rename(old_name, new_name)
            self.history.append(f"Переименован: {old_name} -> {new_name}")
            self.update_history()
            self.current_file = new_name
            self.selected_file_label.setText(f"Имя файла: {new_name}")
        except FileNotFoundError:
            self.notify("Файл не найден.")
        except PermissionError:
            self.notify("Нет разрешения.")
        except Exception as e:
            self.notify(f"Ошибка: {str(e)}")

    def update_watched_folder(self):
        self.watcher.removePaths(self.watcher.directories())
        self.watcher.removePaths(self.watcher.files())

        watched_folder = self.settings.rename_folder_path
        if os.path.isdir(watched_folder):
            self.watcher.addPath(watched_folder)
            print(f"Наблюдаем за папкой: {watched_folder}")
            self.watcher.directoryChanged.connect(self.on_directory_changed)


    def hash_file(self, filepath):
        hasher = hashlib.md5()
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(4096):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except:
            return None  # поврежденный файл

    def rename_new_files(self, folder_path):
        try:
            valid_extensions = ('.epub', '.fb2', '.rtf', '.mobi', '.fb3')
            files_to_process = [
                f for f in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, f)) and 
                f.lower().endswith(valid_extensions)
            ]

            for file_name in files_to_process:
                file_path = os.path.normpath(os.path.join(folder_path, file_name))
                file_ext = os.path.splitext(file_path)[1].lower()

                file_hash = self.hash_file(file_path)
                if not file_hash or file_hash in self.processed_files:
                    continue

                try:
                    decompressor = self.decompressor_factory.get_decompressor(file_path)
                    book = decompressor.decompress(file_path)

                    new_name = self.renamer.create_name(book)
                    new_file_path = os.path.join(folder_path, new_name + file_ext)
                    new_file_path = os.path.normpath(new_file_path)

                    if file_path == new_file_path:
                        self.processed_files.append(file_hash)
                        self.save_processed_files()
                        continue

                    if os.path.exists(new_file_path):
                        print(f"Файл уже существует: {new_file_path}")
                        continue

                    os.rename(file_path, new_file_path)
                    self.processed_files.append(file_hash)
                    self.save_processed_files()
                    print(f"Успешно переименован: {file_name} -> {new_name}{file_ext}")

                except FileNotFoundError as e:
                    print(f"Файл повреждён ({file_ext}): {file_name} — {e}")
                except Exception as e:
                    print(f"Ошибка обработки {file_ext}-файла {file_name}: {e}")
                    continue

        except Exception as e:
            print(f"Критическая ошибка при сканировании папки: {e}")



    def on_directory_changed(self, path):
        print(f"Обнаружены изменения в папке: {path}")
        self.rename_new_files(path)

    def update_history(self):
        self.history_text.clear()
        self.history_text.setPlainText("\n".join(self.history))

    def notify(self, message):
        self.history.append(f"Ошибка: {message}")
        self.update_history()



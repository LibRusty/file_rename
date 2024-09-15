from book import Book
from epub_decompressor import EpubDecompressor
from decompressor_factory import DecompressorFactory
from renamer import Renamer
from settings import Settings
import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTreeView, QFileSystemModel, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QHBoxLayout
)
from PyQt5.QtCore import Qt, QDir


class MainWindow(QMainWindow):
    def __init__(self, settings):
        super().__init__()
        self.decompressor_factory = DecompressorFactory()
        self.settings = settings
        self.renamer = Renamer(self.settings)
        self.settings.add_observer(self)

        self.history = []  # Для хранения истории операций
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setMinimumSize(640, 480)  # Минимальный размер окна 640x480
        self.resize(1600, 1000)

        layout = QHBoxLayout(central_widget)

        # Левое окно: дерево каталогов
        self.dir_model = QFileSystemModel()
        self.dir_model.setFilter(QDir.NoDotAndDotDot |QDir.AllDirs | QDir.AllEntries)
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
        self.resize(800, 600)

    def on_tree_item_click(self, index):
        # Получаем полный путь к выбранному элементу
        file_path = self.dir_model.filePath(index)
        self.selected_file_label.setText(f"Имя файла: {file_path}")
        self.current_file = file_path
        if os.path.isfile(self.current_file):
            self.decompressor = self.decompressor_factory.get_decompressor(self.current_file)
            self.book = self.decompressor.decompress(self.current_file)
            self.new_file_name_input.setText(self.renamer.create_name(self.book))

    def rename_selected_file(self):
        if not hasattr(self, 'current_file'):
            self.notify("Файл не выбран.")
            return

        new_name = self.new_file_name_input.text().strip()
        if not new_name:
            self.notify("Новое имя не может быть пустым.")
            return

        new_file_path = os.path.join(os.path.dirname(self.current_file), new_name)
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

    def update_history(self):
        self.history_text.clear()
        self.history_text.setPlainText("\n".join(self.history))

    def notify(self, message):
        self.history.append(f"Ошибка: {message}")
        self.update_history()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings = Settings()
    window = MainWindow(settings)
    window.show()
    sys.exit(app.exec_())

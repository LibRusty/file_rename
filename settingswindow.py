from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QComboBox, QCheckBox, QLineEdit
)
from PyQt5.QtCore import Qt
from settings import Settings

class SettingsWindow(QMainWindow):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.setMinimumSize(300, 200)

        self.settings = settings

        widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Путь к папке для переименования:"))
        self.folder_path_input = QLineEdit(self.settings.rename_folder_path)
        layout.addWidget(self.folder_path_input)

        select_folder_button = QPushButton("Выбрать папку")
        select_folder_button.clicked.connect(self.select_folder)
        layout.addWidget(select_folder_button)

        layout.addWidget(QLabel("Формат ФИО:"))
        self.fio_format_combobox = QComboBox()
        self.fio_format_combobox.addItems([
            "Фамилия Имя Отчество", 
            "Имя Отчество Фамилия", 
            "Фамилия Имя"
        ])

        self.fio_format_combobox.setCurrentIndex(self.settings.fio_format)
        layout.addWidget(self.fio_format_combobox)

        layout.addWidget(QLabel("Разделитель:"))
        self.separator_combobox = QComboBox()
        self.separator_combobox.addItems(["Тире", "Пробел", "Нижнее подчеркивание"])  # Названия разделителей
        layout.addWidget(self.separator_combobox)

        current_separator = self.settings.separator
        if current_separator == "-":
            self.separator_combobox.setCurrentText("Тире")
        elif current_separator == " ":
            self.separator_combobox.setCurrentText("Пробел")
        elif current_separator == "_":
            self.separator_combobox.setCurrentText("Нижнее подчеркивание")

        layout.addWidget(QLabel("Показывать серии книг:"))
        self.series_checkbox = QCheckBox("Включить отображение серий")
        self.series_checkbox.setChecked(self.settings.series_position == 1)  # Загружаем значение из настроек
        layout.addWidget(self.series_checkbox)

        layout.addWidget(QLabel("Положение заголовка книги:"))
        self.title_position_combobox = QComboBox()
        self.title_position_combobox.addItems(["После автора", "Перед автором"])
        self.title_position_combobox.setCurrentIndex(self.settings.title_position)
        layout.addWidget(self.title_position_combobox)

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
    def select_folder(self):
        from PyQt5.QtWidgets import QFileDialog
        folder = QFileDialog.getExistingDirectory(self, "Выбрать папку")
        if folder:
            self.folder_path_input.setText(folder)

    def save_settings(self):
        fio_format = self.fio_format_combobox.currentIndex()
        selected_separator = self.separator_combobox.currentText()  # Получаем название разделителя
        # Соответствие названий разделителей и символов
        separator_map = {
            "Тире": "-",
            "Пробел": " ",
            "Нижнее подчеркивание": "_"
        }
        separator = separator_map[selected_separator]  # Получаем символ разделителя
        series_position = 1 if self.series_checkbox.isChecked() else 0
        title_position = self.title_position_combobox.currentIndex()
        rename_folder_path = self.folder_path_input.text().strip()
        self.parent().update_watched_folder()

        self.settings.update_settings(
            fio_format=fio_format,
            separator=separator,  # Используем символ разделителя
            series_position=series_position,
            title_position=title_position,
            rename_folder_path=rename_folder_path
        )
        self.parent().rename_new_files(rename_folder_path)

        print("Настройки сохранены:")
        print(f"Формат ФИО: {fio_format}")
        print(f"Разделитель: '{separator}'")
        print(f"Показывать серии книг: {series_position}")
        print(f"Положение заголовка книги: {title_position}")
        print(f"Путь к папке: {rename_folder_path}")

        self.close()

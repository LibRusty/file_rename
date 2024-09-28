from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QComboBox, QCheckBox
)
from PyQt5.QtCore import Qt
from settings import Settings

class SettingsWindow(QMainWindow):
    def __init__(self, settings):
        super().__init__()
        self.setWindowTitle("Настройки")
        self.setMinimumSize(300, 200)

        # Получаем объект настроек
        self.settings = settings

        # Создаем главный виджет
        widget = QWidget()
        layout = QVBoxLayout()

        # Выбор формата ФИО (ComboBox)
        layout.addWidget(QLabel("Формат ФИО:"))
        self.fio_format_combobox = QComboBox()
        self.fio_format_combobox.addItems([
            "Фамилия Имя Отчество", 
            "Имя Отчество Фамилия", 
            "Фамилия Имя"
        ])
        # Устанавливаем текущее значение из настроек
        self.fio_format_combobox.setCurrentIndex(self.settings.fio_format)
        layout.addWidget(self.fio_format_combobox)

        # Выбор разделителя (ComboBox)
        layout.addWidget(QLabel("Разделитель:"))
        self.separator_combobox = QComboBox()
        self.separator_combobox.addItems(["Тире", "Пробел", "Нижнее подчеркивание"])  # Названия разделителей
        layout.addWidget(self.separator_combobox)

        # Устанавливаем текущее значение из настроек
        current_separator = self.settings.separator
        if current_separator == "-":
            self.separator_combobox.setCurrentText("Тире")
        elif current_separator == " ":
            self.separator_combobox.setCurrentText("Пробел")
        elif current_separator == "_":
            self.separator_combobox.setCurrentText("Нижнее подчеркивание")

        # Флажок для отображения серии книг
        layout.addWidget(QLabel("Показывать серии книг:"))
        self.series_checkbox = QCheckBox("Включить отображение серий")
        self.series_checkbox.setChecked(self.settings.series_position == 1)  # Загружаем значение из настроек
        layout.addWidget(self.series_checkbox)

        # Выбор положения заголовка книги (ComboBox)
        layout.addWidget(QLabel("Положение заголовка книги:"))
        self.title_position_combobox = QComboBox()
        self.title_position_combobox.addItems(["После автора", "Перед автором"])
        # Устанавливаем текущее значение из настроек
        self.title_position_combobox.setCurrentIndex(self.settings.title_position)
        layout.addWidget(self.title_position_combobox)

        # Кнопка для сохранения настроек
        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        # Кнопка для закрытия окна
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def save_settings(self):
        # Получаем данные из элементов интерфейса и сохраняем их в настройки
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

        # Обновляем объект Settings
        self.settings.update_settings(
            fio_format=fio_format,
            separator=separator,  # Используем символ разделителя
            series_position=series_position,
            title_position=title_position
        )

        # Выводим сообщение для проверки
        print("Настройки сохранены:")
        print(f"Формат ФИО: {fio_format}")
        print(f"Разделитель: '{separator}'")
        print(f"Показывать серии книг: {series_position}")
        print(f"Положение заголовка книги: {title_position}")

        self.close()

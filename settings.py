from PyQt5.QtCore import QSettings
from observer import Observer

class Settings:
    _instance = None

    def __init__(self):
        self.settings = QSettings("Librust Company", "File Renamer")

        self.fio_format = self.settings.value("fio_format", 0, type=int)
        self.separator = self.settings.value("separator", ' ', type=str)
        self.title_position = self.settings.value("title_position", 0, type=int)
        self.series_position = self.settings.value("series_position", 0, type=int)

        self._observers = []

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
    """
    def notify_observers(self):
        for observer in self._observers:
            observer.update(self.settings)"""

    def update_settings(self, fio_format=None, separator=None, title_position=None, series_position=None):
        if fio_format is not None:
            self.fio_format = fio_format
            self.settings.setValue("fio_format", fio_format)

        if separator is not None:
            self.separator = separator
            self.settings.setValue("separator", separator)

        if title_position is not None:
            self.title_position = title_position
            self.settings.setValue("title_position", title_position)

        if series_position is not None:
            self.series_position = series_position
            self.settings.setValue("series_position", series_position)

        #self.notify_observers()

    def load_settings(self):
        self.fio_format = self.settings.value("fio_format", 0, type=int)
        self.separator = self.settings.value("separator", ' ', type=str)
        self.title_position = self.settings.value("title_position", 0, type=int)
        self.series_position = self.settings.value("series_position", 0, type=int)
        #self.notify_observers()

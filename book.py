from typing import Any

class Book:
    def __init__(self, name, author, series):
        if not name:
            self.name = "Без названия"
        else:
            self.name = name
        if not author:
            self.author = "Неизвестный"
        else:
            self.author = author
        if not series:
            self.series = "Неизвестно"
        else:
            self.series = series
    def get_name(self):
        return self.name
    def get_author(self):
        return self.author
    def get_series(self):
        return self.series
    
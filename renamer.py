from observer import Observer

class Renamer(Observer):
    def __init__(self, settings):
        self.settings = settings
        self.settings.add_observer(self)

    def update(self, settings):
        self.settings = settings

    def create_name(self, book):
        if not book:
            return ''

        author = book.get_author().split()
        title = book.get_name() or "Unknown Title"
        series = book.get_series() or "Unknown Series"

        separator = self.settings.separator
        fio_format = self.settings.fio_format
        title_position = self.settings.title_position
        series_position = self.settings.series_position

        newFIO = self._format_author(author, fio_format, separator)
        newTIT = separator.join(title.split())
        newSer = self._format_series(series, newTIT, series_position, separator)

        return self._combine_name(newFIO, newSer, title_position, separator)

    def _format_author(self, author, fio_format, separator):
        if not author:
            return "Unknown Author"

        if fio_format == 0:  # Фамилия Имя Отчество
            newFIO = f"{author[0]}{separator}{author[1]}"
            if len(author) > 2:
                newFIO += f"{separator}{author[2]}"
        elif fio_format == 1:  # Имя Отчество Фамилия
            newFIO = f"{author[1]}{separator}{author[2]}{separator}{author[0]}" if len(author) > 2 else f"{author[1]}{separator}{author[0]}"
        elif fio_format == 2:  # Фамилия Имя
            newFIO = f"{author[0]}{separator}{author[1]}"
        else:  # Дефолтный формат
            newFIO = f"{author[0]}{separator}{author[1]}"

        return newFIO

    def _format_series(self, series, newTIT, series_position, separator):
        if series_position == 0:
            newSer = f"{newTIT}{separator}Серия{separator}№{separator}{series}"
        else:
            newSer = f"Серия{separator}№{separator}{series}{separator}{newTIT}"
        return newSer

    def _combine_name(self, newFIO, newSer, title_position, separator):
        if title_position == 0:
            name = f"{newFIO}{separator}{newSer}"
        else:
            name = f"{newSer}{separator}{newFIO}"
        return name

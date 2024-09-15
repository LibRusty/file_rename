from settings import Settings
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
        title = book.get_name()
        series = book.get_series() or "Unknown"

        separator = self.settings.separator
        fio_format = self.settings.fio_format
        title_position = self.settings.title_position
        series_position = self.settings.series_position

        newFIO = self._format_author(author, fio_format, separator)
        newTIT = separator.join(title.split())
        newSer = self._format_series(series, newTIT, series_position, separator)
        
        return self._combine_name(newFIO, newSer, title_position, separator)

    def _format_author(self, author, fio_format, separator):
        if fio_format == 0: #ИОФ
            newFIO = author[0] + separator + author[1]
            if len(author) > 2:
                newFIO += separator + author[2]
        elif fio_format == 1: #ФИО
            if len(author) > 2:
                newFIO += author[2] + separator
            newFIO = author[0] + separator + author[1]
        elif fio_format == 2: #ФИ
            if len(author) > 2:
                newFIO = author[2] + separator + author[0]
            else:
                newFIO = author[1] + separator + author[0]
        else:
            if len(author) > 2:
                newFIO = author[0] + separator + author[2]
            else:
                newFIO = author[0] + separator + author[1]
        return newFIO

    def _format_series(self, series, newTIT, series_position, separator, ):
        if series_position == 0:
            newSer = newTIT + separator + 'Серия' + separator + '№' + separator + series
        else:
            newSer = 'Серия' + separator + '№' + separator + series + separator + newTIT
        return newSer

    def _combine_name(self, newFIO, newSer, title_position, separator):
        if title_position == 0:
            name = newFIO + separator + newSer
        else:
            name = newSer + separator + newFIO
        return name

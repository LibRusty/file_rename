from observer import Observer

class Settings:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Settings, cls).__new__(cls, *args, **kwargs)
            cls._instance.init()
        return cls._instance

    def init(self):
        self.fio_format = 0
        self.separator = ' '
        self.title_position = 0
        self.series_position = 0
        self._observers = []

    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update(self)

    def update_settings(self, fio_format=None, separator=None, title_position=None, series_position=None):
        if fio_format is not None:
            self.fio_format = fio_format
        if separator is not None:
            self.separator = separator
        if title_position is not None:
            self.title_position = title_position
        if series_position is not None:
            self.series_position = series_position

        self.notify_observers()

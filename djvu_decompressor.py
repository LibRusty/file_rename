import subprocess
import shutil
import os
from book import Book
from decompressor import Decompressor

class DjvuDecompressor(Decompressor):
    def decompress(self, name_file):
        # Путь к утилите Calibre ebook-convert
        ebook_convert_path = r"C:\Program Files\Calibre2\ebook-convert.exe"  # Укажите свой путь
        ebook_meta_path = r"C:\Program Files\Calibre2\ebook-meta.exe"  # Укажите свой путь

        # Путь к временному EPUB файлу после конвертации
        temp_epub = name_file + '.epub'

        try:
            # Конвертация DjVu в EPUB с помощью ebook-convert
            command_convert = [
                ebook_convert_path,
                name_file,
                temp_epub
            ]
            subprocess.run(command_convert, check=True)

            # Извлечение метаданных с помощью ebook-meta
            command_meta = [
                ebook_meta_path,
                temp_epub
            ]
            result = subprocess.run(command_meta, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Извлечение информации из stdout результата
            author, title, series = None, None, None

            for line in result.stdout.splitlines():
                if 'Author(s):' in line:
                    author = line.split(':', 1)[1].strip()
                elif 'Title:' in line:
                    title = line.split(':', 1)[1].strip()
                elif 'Series:' in line:
                    series = line.split(':', 1)[1].strip()

            # Удаление временного EPUB файла
            os.remove(temp_epub)

            return Book(title, author, series)

        except subprocess.CalledProcessError as e:
            print(f"Ошибка при конвертации DjVu в EPUB: {e}")
        except Exception as e:
            print(f"Ошибка: {e}")

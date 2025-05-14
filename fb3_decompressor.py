import xml.etree.ElementTree as ET
from decompressor import Decompressor
import os
import shutil
import tempfile
from book import Book
import zipfile

class FB3Decompressor(Decompressor):
    def decompress(self, name_file):
        if not name_file.endswith('.fb3'):
            raise ValueError("Неверный формат файла. Ожидался .fb3")

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_zip_path = os.path.join(tmp_dir, 'temp.zip')
            shutil.copyfile(name_file, temp_zip_path)

            with zipfile.ZipFile(temp_zip_path, 'r') as myzip:
                myzip.extractall(tmp_dir)

            ops_path = os.path.join(tmp_dir, 'fb3', 'description.xml')

            if not os.path.exists(ops_path):
                raise FileNotFoundError("Файл description.xml не найден в архиве")

            tree = ET.parse(ops_path)
            root = tree.getroot()

            ns = {'ns': 'http://www.fictionbook.org/FictionBook3/description'}

            # Название книги
            title_elem = root.find('ns:title/ns:main', namespaces=ns)
            title = title_elem.text.strip() if title_elem is not None else None

            # Название серии
            series_elem = root.find('ns:sequence/ns:title/ns:main', namespaces=ns)
            series = series_elem.text.strip() if series_elem is not None else None

            # Поиск автора
            subject_elem = root.find('ns:fb3-relations/ns:subject[@link="author"]', namespaces=ns)
            if subject_elem is not None:
                first_name_elem = subject_elem.find('ns:first-name', namespaces=ns)
                last_name_elem = subject_elem.find('ns:last-name', namespaces=ns)
                if first_name_elem is not None and last_name_elem is not None:
                    first_name = first_name_elem.text.strip()
                    last_name = last_name_elem.text.strip()
                    author = f"{last_name} {first_name}"
                else:
                    # fallback через title/main
                    author_elem = subject_elem.find('ns:title/ns:main', namespaces=ns)
                    author = author_elem.text.strip() if author_elem is not None else None
            else:
                author = None

        return Book(title, author, series)

from lxml import etree
from decompressor import Decompressor
from book import Book
import re

class FB2Decompressor(Decompressor):
    def decompress(self, file_path):
        with open(file_path, 'rb') as fb2_file:
            tree = etree.parse(fb2_file)
            root = tree.getroot()

            description = root.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}description')
            if description is None:
                raise ValueError("Invalid FB2 file: missing <description> tag.")

            title = self._get_title(description)
            series = self._get_series(description)
            author = self._get_author(description)

            return Book(title, author, series)

    def _get_title(self, description):
        title_info = description.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}title-info')
        if title_info is not None:
            book_title = title_info.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}book-title')
            return book_title.text.strip() if book_title is not None and book_title.text else "Unknown Title"
        return "Unknown Title"

    def _get_series(self, description):
        title_info = description.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}title-info')
        if title_info is not None:
            series_info = title_info.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}sequence')
            if series_info is not None:
                series_name = series_info.get("name")
                series_number = series_info.get("number")

                if series_number:
                    return series_number

                if series_name:
                    match = re.search(r'\d+', series_name)
                    if match:
                        return match.group(0)

        return "Unknown Series"

    def _get_author(self, description):
        title_info = description.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}title-info')
        if title_info is not None:
            author_first_name = title_info.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}first-name')
            author_last_name = title_info.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}last-name')
            if author_first_name is not None and author_last_name is not None:
                return f"{author_first_name.text.strip()} {author_last_name.text.strip()}"
        return "Unknown Author"


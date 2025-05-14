from pathlib import PurePath
from decompressor import Decompressor
from book import Book
import re
import pdfplumber

class PdfDecompressor(Decompressor):
    def decompress(self, name_file):
        with pdfplumber.open(name_file) as pdf:
            text = ""
            for page in pdf.pages[:10]:  # читаем первые 10 страниц
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            lines = [line.strip() for line in text.split('\n') if line.strip()]
            author, title, series = self._parse_metadata(lines)
            return Book(title, author, series)

    def _parse_metadata(self, lines):
        ignore_words = [
            'министерство', 'федерация', 'университет', 'академия',
            'институт', 'кафедра', 'факультет', 'образования',
            'российская', 'рф', 'государственный', 'науки', 'вуз',
            'isbn', 'удк', 'ббк', '©', 'перевод', 'вступительная статья'
        ]

        potential_authors = []
        title_block = []
        found_author_index = -1

        for i, line in enumerate(lines[:50]):
            l = line.lower()
            if any(w in l for w in ignore_words):
                continue

            if re.match(r'^[А-ЯЁ][а-яё]+ [А-ЯЁ]\.?[А-ЯЁ]\.?$', line) or \
               re.match(r'^[А-ЯЁ]\.?[А-ЯЁ]\.? [А-ЯЁ][а-яё]+$', line) or \
               re.match(r'^[A-Z][a-z]+\s+[A-Z][a-z]+$', line):
                potential_authors.append(self._clean_text(line))
                found_author_index = i
                break

        if found_author_index != -1:
            for line in lines[found_author_index + 1:found_author_index + 10]:  # увеличиваем до 10 строк
                if not line.strip():
                    break
                if any(w in line.lower() for w in ignore_words):
                    continue
                title_block.append(line.strip())


        if not potential_authors and len(lines) > 0:
            potential_authors.append(self._clean_text(lines[0]))
        if not title_block and len(lines) > 1:
            title_block = [self._clean_text(lines[1])]

        author = potential_authors[0] if potential_authors else None
        title = ' '.join(title_block) if title_block else None

   
        series = None
        if title and '(' in title:
            m = re.search(r'\((.*?)\)', title)
            if m:
                series = m.group(1)
                title = re.sub(r'\s*\(.*?\)\s*', ' ', title).strip()


        title = self._remove_arifacts(title)

        return author, self._clean_text(title) if title else None, series

    def _clean_text(self, text):
        return re.sub(r'\s+', ' ', text).strip()

    def _remove_arifacts(self, text):
        text = re.sub(r'cid\?[a-zA-Z0-9]+', '', text) 
        text = re.sub(r'\s+', ' ', text) 
        return text

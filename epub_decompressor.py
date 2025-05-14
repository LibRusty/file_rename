from decompressor import Decompressor
import os
import shutil
import tempfile
from book import Book
import zipfile


class EpubDecompressor(Decompressor):
    def decompress(self, name_file):
        if not name_file.endswith('.epub'):
            raise ValueError("Неверный формат файла. Ожидался .epub")

        with tempfile.TemporaryDirectory() as tmp_dir:
            temp_zip_path = os.path.join(tmp_dir, 'temp.zip')
            shutil.copyfile(name_file, temp_zip_path)

            with zipfile.ZipFile(temp_zip_path, 'r') as myzip:
                myzip.extractall(tmp_dir)

            ops_path = os.path.join(tmp_dir, 'OPS', 'content.opf')

            if not os.path.exists(ops_path):
                raise FileNotFoundError("Файл content.opf не найден в архиве")

            author, title, series = None, None, None
            with open(ops_path, encoding="utf-8", errors='replace') as g:
                for data in g:
                    j = self.KMP(data, 'creator>')
                    i = self.KMP(data, 'title>')
                    k = self.KMP(data, 'sequence')

                    if j != -1:
                        j += 8
                        end_j = data.find('<', j)
                        author = data[j:end_j].strip()

                    if i != -1:
                        i += 6
                        end_i = data.find('<', i)
                        title = data[i:end_i].strip()

                    if k != -1:
                        k1 = self.KMP(data, 'number')
                        if k1 != -1:
                            k1 += 7
                            end_k1 = data.find('\"', k1)
                            series = data[k1:end_k1].strip()

                    if author and title and series:
                        break

        return Book(title, author, series)

    @staticmethod
    def KMP(text, pattern):
        n, m = len(text), len(pattern)
        lps = [0] * m
        j = 0

        for i in range(1, m):
            while j > 0 and pattern[i] != pattern[j]:
                j = lps[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
                lps[i] = j

        j = 0
        for i in range(n):
            while j > 0 and text[i] != pattern[j]:
                j = lps[j - 1]
            if text[i] == pattern[j]:
                j += 1
                if j == m:
                    return i - m + 1
        return -1

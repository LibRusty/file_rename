from decompressor import Decompressor
import os
import shutil
import tempfile
from book import Book
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class MobiDecompressor(Decompressor):
    def decompress(self, name_file):
        if not name_file.endswith('.mobi'):
            raise ValueError("Неверный формат файла. Ожидался .mobi")

        with tempfile.TemporaryDirectory() as tmp_dir:
            if hasattr(sys, '_MEIPASS'):
                kindleunpack_path = os.path.join(sys._MEIPASS, "KindleUnpack", "lib", "kindleunpack.py")
            else:
                kindleunpack_path = os.path.join(BASE_DIR, "KindleUnpack", "lib", "kindleunpack.py")

            subprocess.run([
                sys.executable,
                kindleunpack_path,
                name_file,
                tmp_dir
            ], cwd=BASE_DIR)

            mobi_path = os.path.join(tmp_dir, 'mobi7', 'content.opf')
            if not os.path.exists(mobi_path):
                mobi_path = os.path.join(tmp_dir, 'mobi8', 'content.opf')
                if not os.path.exists(mobi_path):
                    raise FileNotFoundError("Файл content.opf не найден в архиве")

            author, title, series = None, None, None
            with open(mobi_path, encoding="utf-8", errors='replace') as g:
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

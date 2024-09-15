from decompressor import Decompressor
import os
import shutil
import tempfile
from book import Book
from pathlib import PurePath
import zipfile
import posixpath as zip_path

class EpubDecompressor(Decompressor):
    def decompress(self, name_file):
        new_name = name_file + 'NEW.epub'
        shutil.copyfile(name_file, new_name)
        name = (new_name)[:-4] + 'zip'
        os.rename(new_name, name)

        with tempfile.TemporaryDirectory() as tmp_dir:
            with zipfile.ZipFile(name, 'r') as myzip:
                myzip.extractall(tmp_dir)

            ops_path = os.path.join(tmp_dir, 'OPS', 'content.opf')
            with open(ops_path, encoding="utf-8", errors='replace') as g:
                author, title, series = None, None, None
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

        os.remove(name)  # Удаление временного ZIP файла
        return Book(title, author, series)
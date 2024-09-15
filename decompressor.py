from pathlib import PurePath
import zipfile
import posixpath as zip_path
import os
import shutil
import tempfile
from book import Book

class Decompressor:
    def decompress(self, name_file):
        raise NotImplementedError("This method should be overridden.")
    def KMP(self, text, pattern):
        if not pattern:
            print('The pattern occurs with shift 0')
            return -1

        if not text or len(pattern) > len(text):
            print('Pattern not found')
            return -1

        chars = list(pattern)
        next = [0] * (len(pattern) + 1)

        for i in range(1, len(pattern)):
            j = next[i]

            while j > 0 and chars[j] != chars[i]:
                j = next[j]

            if j > 0 or chars[j] == chars[i]:
                next[i + 1] = j + 1

        i, j = 0, 0
        while i < len(text):
            if j < len(pattern) and text[i] == pattern[j]:
                j = j + 1
                if j == len(pattern):
                    return i - j + 1
            elif j > 0:
                j = next[j]
                i = i - 1
            i = i + 1
        return -1

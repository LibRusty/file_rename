from striprtf.striprtf import rtf_to_text
from pathlib import PurePath
from decompressor import Decompressor
from book import Book
import os

class RtfDecompressor(Decompressor):
    def decompress(self, name_file):
        with open(name_file, 'rb') as rtf_file:
            rtf_content = rtf_file.read().decode('windows-1251')  
            text = rtf_to_text(rtf_content)
        
        lines = text.split("\n")
        author = lines[0].strip() if len(lines) > 0 else None
        title = lines[1].strip() if len(lines) > 1 else None  
        series = None
        if title and '(' in title and ')' in title:
            start = title.find('(') + 1
            end = title.find(')', start)
            series = title[start:end]
            title = title[:start-1] + title[end+1:].strip()
        
        return Book(title, author, series)

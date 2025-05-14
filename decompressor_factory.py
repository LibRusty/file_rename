from epub_decompressor import EpubDecompressor
from fb2_decompressor import FB2Decompressor
from rtf_decompressor import RtfDecompressor
from pdf_decompressor import PdfDecompressor
from mobi_decompressor import MobiDecompressor
from fb3_decompressor import FB3Decompressor
from decompressor import Decompressor

class DecompressorFactory:
    def get_decompressor(self, file_name) -> Decompressor:
        if file_name.endswith('.epub'):
            return EpubDecompressor()
        elif file_name.endswith('.fb2'):
            return FB2Decompressor()
        elif file_name.endswith('.rtf'):
            return RtfDecompressor()
        elif file_name.endswith('.pdf'):
            return PdfDecompressor()
        elif file_name.endswith('.mobi'):
            return MobiDecompressor()
        elif file_name.endswith('.fb3'):
            return FB3Decompressor()
        else:
            raise ValueError("Unsupported file format")

from epub_decompressor import EpubDecompressor
from decompressor import Decompressor

class DecompressorFactory:
    def get_decompressor(self, file_name) -> Decompressor:
        if file_name.endswith('.epub'):
            return EpubDecompressor()
        else:
            raise ValueError("Unsupported file format")

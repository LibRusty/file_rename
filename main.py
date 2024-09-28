from book import Book
from epub_decompressor import EpubDecompressor
from decompressor_factory import DecompressorFactory
from renamer import Renamer
from settings import Settings
from settingswindow import SettingsWindow
import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTreeView, QFileSystemModel, QVBoxLayout, QWidget, QLabel, 
    QLineEdit, QPushButton, QTextEdit, QHBoxLayout, QAction
)
from PyQt5.QtCore import Qt, QDir
from mainwindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings = Settings()
    window = MainWindow(settings)
    window.show()
    sys.exit(app.exec_())
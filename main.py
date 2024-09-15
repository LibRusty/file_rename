import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QFileDialog, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QMessageBox
from PyQt5.QtWidgets import QGridLayout, QRadioButton, QWidget, QDialog, QFrame, QButtonGroup
import book
from book import *
import sys
import re

class Setting(QDialog):
    def __init__(self, parent = None):
        super(Setting, self).__init__(parent)
        self.parent = parent;
        self.setWindowTitle("Настройки")
        self.setGeometry(1000, 400, 500, 500)
        self.a, self.b, self.c, self.d, self.e = parent.GetSetting()

        layout = QGridLayout(self)
        self.setLayout(layout)
        layout.setHorizontalSpacing(3)
        layout.setVerticalSpacing(3)
        

        FNS_text = QtWidgets.QLabel(self)
        FNS_text.setText("Порядок ФИО автора")
        layout.addWidget(FNS_text, 0, 0)
        
        self.FNS_ = QButtonGroup(self)

        FNS_0 = QRadioButton("ИОФ", self)
        self.FNS_.addButton(FNS_0)
        FNS_0.id = 0;
        FNS_0.clicked.connect(self.FNSonClicked)
        layout.addWidget(FNS_0, 1, 0)
        FNS_1 = QRadioButton("ФИО",self)
        self.FNS_.addButton(FNS_1)
        FNS_1.id = 1;
        FNS_1.clicked.connect(self.FNSonClicked)
        layout.addWidget(FNS_1, 1, 1)
        FNS_2 = QRadioButton("ФИ", self)
        self.FNS_.addButton(FNS_2)
        FNS_2.id = 2;
        FNS_2.clicked.connect(self.FNSonClicked)
        layout.addWidget(FNS_2, 1, 2)
        FNS_3 = QRadioButton("ИФ", self)
        self.FNS_.addButton(FNS_3)
        FNS_3.id = 3;
        FNS_3.clicked.connect(self.FNSonClicked)
        layout.addWidget(FNS_3, 1, 3)

        FNS_array = [FNS_0, FNS_1, FNS_2, FNS_3]
        FNS_array[self.a].click()

        self.FNS_.buttonPressed.connect(self.enable)

        SEP_text = QtWidgets.QLabel("Разделитель между словами",self)
        layout.addWidget(SEP_text, 2, 0)
        
        self.SEP_ = QButtonGroup(self)
        SEP_0 = QRadioButton("Нижнее подчеркивание", self)
        SEP_0.id = "_"
        SEP_0.clicked.connect(self.SEPonClicked)
        self.SEP_.addButton(SEP_0)
        layout.addWidget(SEP_0, 3, 0)
        SEP_1 = QRadioButton("Тире", self)
        SEP_1.id = "-"
        SEP_1.clicked.connect(self.SEPonClicked)
        self.SEP_.addButton(SEP_1)
        layout.addWidget(SEP_1, 3, 1)
        SEP_2 = QRadioButton("Пробел", self)
        SEP_2.id = " "
        SEP_2.clicked.connect(self.SEPonClicked)
        self.SEP_.addButton(SEP_2)
        layout.addWidget(SEP_2, 3, 2)

        if self.b == '_':
            SEP_0.click()
        elif self.b == '-':
            SEP_1.click()
        else:
            SEP_2.click()

        self.SEP_.buttonPressed.connect(self.enable)

        SER_text = QtWidgets.QLabel("Запись серии и названия книги", self)
        self.SER_ = QButtonGroup(self)
        layout.addWidget(SER_text, 4, 0)
        SER_0 = QRadioButton("Вначале название книги, затем серия", self)
        SER_0.id = 0
        SER_0.clicked.connect(self.SERonClicked)
        self.SER_.addButton(SER_0)
        layout.addWidget(SER_0, 5, 0)
        SER_1 = QRadioButton("Вначале серия книги, затем название", self)
        SER_1.id = 1
        SER_0.clicked.connect(self.SERonClicked)
        self.SER_.addButton(SER_1)
        layout.addWidget(SER_1, 5, 1)

        SER_array = [SER_0, SER_1]
        SER_array[self.c].click()
        
        self.SER_.buttonPressed.connect(self.enable)

        self.TIT_ = QButtonGroup(self)
        TIT_text = QtWidgets.QLabel("Запись названия и автора книги", self)
        layout.addWidget(TIT_text, 6, 0)
        TIT_0 = QRadioButton("Вначале автор книги, затем название", self)
        TIT_0.id = 0
        TIT_0.clicked.connect(self.TITonClicked)
        self.TIT_.addButton(TIT_0)
        layout.addWidget(TIT_0, 7, 0)
        TIT_1 = QRadioButton("Вначале название книги, затем автор", self)
        TIT_1.id = 1
        TIT_1.clicked.connect(self.TITonClicked)
        self.TIT_.addButton(TIT_1)
        layout.addWidget(TIT_1, 7, 1)   

        TIT_array = [TIT_0, TIT_1]
        TIT_array[self.d].click()
        
        self.TIT_.buttonPressed.connect(self.enable)

        self.path_txt = QtWidgets.QPushButton("Выбрать путь для автоматического переименования файлов", self)
        self.path_txt.clicked.connect(self.open_dir)
        self.path = QLineEdit(self)
        self.path.setText(self.e)
        self.path.textChanged.connect(self.enable)

        layout.addWidget(self.path_txt, 8, 0)
        layout.addWidget(self.path, 9, 0)

        self.save = QtWidgets.QPushButton("Сохранить", self)
        self.save.setEnabled(False)
        self.save.clicked.connect(self.setSetting)

        self.notsave = QtWidgets.QPushButton("Выход", self)
        self.notsave.setEnabled(True)
        self.notsave.clicked.connect(self.close)

        layout.addWidget(self.save, 10, 0)
        layout.addWidget(self.notsave, 10, 1)

    def setSetting(self):
        self.parent.SetSetting(self.a, self.b, self.c, self.d, self.e)
        self.save.setEnabled(False)

    def enable(self):
        self.save.setEnabled(True)
    
    def FNSonClicked(self):
        r = self.sender()
        self.a = r.id
    
    def SEPonClicked(self):
        r = self.sender()
        self.b = r.id

    def SERonClicked(self):
        r = self.sender()
        self.c = r.id
    
    def TITonClicked(self):
        r = self.sender()
        self.d = r.id

    def open_dir(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        files = QFileDialog.getExistingDirectory(self, "Выберите папку", "", options=options)
        if files: 
            self.path.setText(files)
            self.e = files

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("booklet")
        self.setGeometry(1200, 250, 500, 500)

        self.btn_open_file = QtWidgets.QPushButton(self)
        self.name_file = QtWidgets.QLineEdit(self)
        self.info_file = QtWidgets.QTextEdit(self)
        self.rename_file = QtWidgets.QPushButton(self)
        self.txt_new_name = QtWidgets.QLabel(self)
        self.new_name = QtWidgets.QLineEdit(self)
        
        self.btn_open_dir = QtWidgets.QPushButton(self)
        self.name_dir = QtWidgets.QLineEdit(self)
        self.rename_dir = QtWidgets.QPushButton(self)

        self.settings0 = QtWidgets.QPushButton(self)

        self.layout1 = QHBoxLayout()
        self.layout2 = QVBoxLayout()
        self.layout3 = QHBoxLayout()
        self.layout4 = QVBoxLayout()
        self.layout0 = QVBoxLayout()
        self.layout00 = QVBoxLayout()
        self.layout30 = QVBoxLayout()

        self.msg = QMessageBox()
        self.msg1 = QMessageBox()
        
        self.fio = 0 #ИОФ - 0, ФИО - 1, ФИ - 2, ИФ - 3
        self.sep = '_'
        self.series = 0; #серия пишется после названия
        self.tit = 0; #название книги пишется после автора

        self.AUTHOR = ''
        self.TITLE = ''
        self.SERIES = ''
        self.PATH = ''

        self.initUI()

    def initUI(self):

        self.btn_open_file.setText("Открыть файл")
        self.btn_open_file.clicked.connect(self.open_file)
        
        self.name_file.setEnabled(True)

        self.info_file.setText("Информация о файле")
        self.info_file.setEnabled(False)

        self.rename_file.setText("Переименовать файл")
        self.rename_file.clicked.connect(self.renamefile)
        
        self.txt_new_name.setText("Новое название файла")
        self.txt_new_name.setVisible(True)

        self.new_name.setEnabled(False)
        self.new_name.setVisible(True)

        self.btn_open_dir.setText("Открыть папку")
        self.btn_open_dir.clicked.connect(self.open_dir)
        
        self.name_dir.setEnabled(True)

        self.rename_dir.setText("Переименовать все файлы в папке")
        self.rename_dir.clicked.connect(self.renamedir)

        self.layout0.addWidget(self.btn_open_dir)
        self.layout0.addWidget(self.name_dir)
        self.layout0.addStretch()
        
        self.layout00.addWidget(self.rename_dir)
        self.layout00.addStretch()

        self.layout1.addLayout(self.layout0)
        self.layout1.addLayout(self.layout00)
        self.layout1.addStretch()

        self.layout2.addWidget(self.btn_open_file)
        self.layout2.addWidget(self.name_file)
        self.layout2.addWidget(self.info_file)
        self.layout2.addStretch()

        
        self.layout30.addWidget(self.txt_new_name)
        self.layout30.addWidget(self.new_name)
        self.layout30.addStretch()

        self.layout3.addLayout(self.layout2)
        self.layout3.addLayout(self.layout30)
        self.layout3.addStretch()


        self.layout40 = QVBoxLayout()
        self.layout40.addWidget(self.rename_file)
        self.layout40.addWidget(self.settings0)
        self.layout40.addStretch()

        self.layout4.addLayout(self.layout1)
        self.layout4.addLayout(self.layout3)
        self.layout4.addLayout(self.layout40)
        self.layout4.addStretch()

        self.settings0.setText("Настройки")
        self.settings0.clicked.connect(self.setting) 

        self.widget = QWidget()
        self.widget.setLayout(self.layout4)
        self.setCentralWidget(self.widget)

        self.msg.setWindowTitle("Ошибка")
        self.msg.setText("В поле ввода пусто")
        self.msg.setIcon(QMessageBox.Warning)

        self.msg1.setWindowTitle("Ошибка")
        self.msg1.setText("Доступ к файлу указан некорректно")
        self.msg1.setIcon(QMessageBox.Warning)
    
    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Открыть файл", "","Epub Files (*.epub)", options=options)
        if fileName:
            self.name_file.setText(fileName)
            author, title, series = get_Epub(fileName)
            self.Write(author, title, series, self.info_file)
            newname = self.create_name(self.name_file.text())
            self.new_name.setText(newname)
        
            
            
    
    def open_dir(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        files = QFileDialog.getExistingDirectory(self, "Выберите папку", "", options=options)
        if files: 
            self.name_dir.setText(files)
            


    def renamefile(self):
        name = self.name_file.text()
        if name:
            if os.path.exists(name):
                self.name_file.setText(rename(name, self.new_name.text()))
            else:
                self.msg1.exec_()
        else:
            self.msg.exec_()

    def renamedir(self):
        name = self.name_dir.text()
        if name:
            if os.path.exists(name):
                for filename in os.listdir(name):
                    if (filename[-5:] == '.epub'):
                        print(filename)
                        filename = name + '/' + filename
                        a, b, c = get_Epub(filename)
                        self.AUTHOR = a
                        self.TITLE = b
                        self.SERIES = c
                        newname = self.create_name('h')
                        rename(filename, newname)
            else:
                self.msg1.exec_()
        else:
            self.msg.exec_()

    
    def Write(self, author, title, series, info):
        text = 'Автор: ' + author + '\n' + 'Название книги: ' + title + '\n' + 'Номер серии: ' + series
        self.AUTHOR = author
        self.TITLE = title
        self.SERIES = series
        info.clear()
        info.setText(text)
        
    def create_name(self, name0):
        if name0:
            IOF = self.AUTHOR.split()
            newFIO = ''
            if self.fio == 0: #ИОФ
                newFIO = IOF[0] + self.sep + IOF[1]
                if len(IOF) > 2:
                    newFIO += self.sep + IOF[2]
            elif self.fio == 1: #ФИО
                if len(IOF) > 2:
                    newFIO += IOF[2] + self.sep
                newFIO = IOF[0] + self.sep + IOF[1]
            elif self.fio == 2: #ФИ
                if len(IOF) > 2:
                    newFIO = IOF[2] + self.sep + IOF[0]
                else:
                    newFIO = IOF[1] + self.sep + IOF[0]
            else:
                if len(IOF) > 2:
                    newFIO = IOF[0] + self.sep + IOF[2]
                else:
                    newFIO = IOF[0] + self.sep + IOF[1]
            
            TIT = self.TITLE.split()
            newTIT = ''
            for i in TIT:
                newTIT += (i + self.sep)
            newTIT = newTIT[:-1]

            if self.series == 0:
                newSer = newTIT + self.sep + 'Серия' + self.sep + '№' + self.sep + self.SERIES
            else:
                newSer = 'Серия' + self.sep + '№' + self.sep + self.SERIES + self.sep + newTIT
            
            if self.tit == 0:
                name = newFIO + self.sep + newSer
            else:
                name = newSer + self.sep + newFIO

            name += '.epub' 
            return name
        else:
            return ''

    def GetSetting(self):
        return self.fio, self.sep, self.series, self.tit, self.PATH
    
    def SetSetting(self, a, b, c, d, e):
        self.fio = a
        self.sep = b
        self.series = c
        self.tit = d
        self.PATH = e

    def setting(self):
        global settings 
        settings = Setting(self);
        settings.show()


def application():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    application()

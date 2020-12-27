#!/usr/bin/env python3

import sys
import os
import urllib.request

from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QSplitter
from PyQt5.QtCore import QObject, QUrl, Qt, pyqtSignal, pyqtSlot, pyqtProperty
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtGui import QIcon, QFont

class PreviewPage(QWebEnginePage):
    pass

class Document(QObject):
    def __init__(self):
        super().__init__()
        self.m_text = ''

    def getText(self):
        return self.m_text

    def setText(self, text):
        if text == self.m_text:
            return
        self.m_text = text
        self.textChanged.emit(self.m_text)

    textChanged = pyqtSignal(str)
    text = pyqtProperty(str, fget=getText, fset=setText, notify=textChanged)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('落雪的修行')
        self.setWindowIcon(QIcon('baby.ico'))
        self.showMaximized()

        self.splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self.splitter)

        self.editor = QPlainTextEdit()
        self.preview = QWebEngineView()
        self.preview.setContextMenuPolicy(Qt.NoContextMenu)

        self.splitter.addWidget(self.editor)
        self.splitter.addWidget(self.preview)

        self.font = QFont()
        self.font.setPointSize(10)
        self.editor.setFont(self.font)
        self.page = PreviewPage()
        self.preview.setPage(self.page)

        self.channel = QWebChannel()
        self.m_content = Document()
        self.channel.registerObject('content', self.m_content)
        self.page.setWebChannel(self.channel)

        self.editor.textChanged.connect(lambda :self.m_content.setText(self.editor.toPlainText()))

        self.url_string = urllib.request.pathname2url(os.path.join(os.getcwd(), "index.html"))
        self.preview.setUrl(QUrl(self.url_string))

        with open(os.getcwd()+'/static/default.md','r', encoding='utf-8') as f:
            self.defaultmd = f.read()
            self.editor.setPlainText(self.defaultmd)

def main(argv):
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    a = QApplication(argv)
    w = MainWindow()
    w.show()
    return a.exec_()

if __name__ == '__main__':
    sys.exit(main(sys.argv))

from PySide6.QtCore import (
    QCoreApplication,
    Qt
)

from PySide6.QtGui import (
    QFont,
    QIcon,
    QKeySequence,
    QTextCharFormat
)

from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget
)

from custom import Highlighter
from parsing_tools import Entry, StyleSheet

IMG_PATH = 'resources/img/'

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CSS Sorter')
        self.resize(920, 480)
        self.setMinimumSize(300, 200)

        self.editor = QPlainTextEdit()
        self.editor.setStyleSheet('font: 10pt "Courier New"')

        self.highlighter = Highlighter()

        self.addHighlightCategories([f'\\b{category}\\b' for category in Entry().get_keys()], Qt.red)
        self.addHighlightCategories([f'#[^\s,]+'], Qt.blue)
        self.addHighlightCategories([f'(?<!\d)\.[^\s,]+\\b'], Qt.darkGreen)

        self.highlighter.setDocument(self.editor.document())

        self.generateMenus()
       
        mainWidget = QWidget()
        mainVerLayout = QVBoxLayout()
        mainVerLayout.addWidget(self.editor)
        mainWidget.setLayout(mainVerLayout)
        self.setCentralWidget(mainWidget)

    def addHighlightCategories(self, categories, color):
        variableFormat = QTextCharFormat()
        variableFormat.setFontWeight(QFont.Bold)
        variableFormat.setForeground(color)
        for category in categories:
            self.highlighter.addMapping(category, variableFormat)

    def generateMenus(self):
        fileMenu = self.menuBar().addMenu(self.tr('File'))
        fileMenu.addAction(QIcon(IMG_PATH + 'document-line.svg'), self.tr('New'), self.onNew, QKeySequence.New)
        fileMenu.addAction(QIcon(IMG_PATH + 'folder-open-line.svg'), self.tr('Open'), self.onOpen, QKeySequence.Open)
        fileMenu.addAction(QIcon(IMG_PATH + 'floppy-line.svg'), self.tr('Save'), self.onSave, QKeySequence.Save)
        fileMenu.addSeparator()
        fileMenu.addAction(QIcon(IMG_PATH + 'power-line.svg'), self.tr('Exit'), self.onExit)
        toolsMenu = self.menuBar().addMenu(self.tr('Tools'))
        toolsMenu.addAction(self.tr('Format'), self.onFormat)

    def onNew(self):
        pass

    def onOpen(self):
        fileName = QFileDialog.getOpenFileName(self, self.tr('Open File'), '/', self.tr("Cascade Style Sheet (*.css)"))
        if fileName and fileName[0]:
            with open(fileName[0]) as f:
                self.editor.setPlainText(f.read())

    def onFormat(self):
        css = StyleSheet(self.editor.toPlainText())
        css.parse()
        self.editor.setPlainText(css.generate_output())


    def onSave(self):
        pass

    def onExit(self):
        if self.close():
            QApplication.quit()

def main():
    import sys
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

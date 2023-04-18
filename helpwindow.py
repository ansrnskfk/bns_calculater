from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
import sys

form_helpnwindow = uic.loadUiType('ui/helpwindow.ui')[0]


class HelpWindow(QWidget, form_helpnwindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.setWindowTitle('블소 계산기')

        # 도움 이미지 추가
        self.pix_help = QPixmap('/img/help.png')
        self.lbl_img.setPixmap(self.pix_help)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('/img/icon.png'))
    helpwindow = HelpWindow()
    helpwindow.show()
    app.exec_()
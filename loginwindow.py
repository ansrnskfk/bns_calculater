from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import webbrowser
import sys
import getmarket
import helpwindow
import calcwindow

form_loginwindow = uic.loadUiType('loginwindow.ui')[0]
print(uic.__file__)


class LoginWindow(QWidget, form_loginwindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.setWindowTitle('블소 계산기')

        # 사용 방법 버튼
        self.btn_help.clicked.connect(self.open_helpwindow)

        # 공홈 및 웹 시장 열기 버튼
        self.btn_bns_web.clicked.connect(self.open_bns_url)
        self.btn_market.clicked.connect(self.open_market_url)

        # 토큰 입력, 토큰 검증
        self.le_input_token.returnPressed.connect(self.token_check)
        self.btn_token_check.clicked.connect(self.token_check)

        # 로그인 버튼
        self.btn_login.clicked.connect(self.change_calcwindow)

    # 사용방법 창 열기
    def open_helpwindow(self):
        self.help = helpwindow.HelpWindow()

    # 블소 공식 홈페이지 열기
    def open_bns_url(self):
        webbrowser.open_new('https://bns.plaync.com/')

    # 시장 웹페이지 열기
    def open_market_url(self):
        webbrowser.open('https://g-bnsmarket.plaync.com/bns/bidder/home.web')

    # 토큰 검증
    def token_check(self):
        self.token = self.le_input_token.text()
        self.cls_market = getmarket.GetMarketInfo()
        self.check_result = self.cls_market.token_check(self.token)

        if self.check_result:
            QMessageBox.information(self, 'success', '검증 성공')
            self.check = True
        else:
            QMessageBox.warning(self, 'error', '검증 실패')
            self.check = False

    # 계산기 창으로 넘어가기
    def change_calcwindow(self):
        if self.check:
            self.materials = self.cls_market.get_material(self.token)
            self.hide()
            self.clac = calcwindow.CalcWindow(self.materials, self.token)
        else:
            QMessageBox.warning(self, 'error', '토큰 검증을 먼저 해주십시오.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.png'))
    loginwindow = LoginWindow()
    app.exec_()
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import sys
import pymysql
import getmarket

form_calcwindow = uic.loadUiType('calcwindow.ui')[0]

con = pymysql.connect(host='127.0.0.1', user='bns_db', password='336677', db='bns_calculater', charset='utf8')
cur = con.cursor()


class CalcWindow(QWidget, form_calcwindow):

    def __init__(self, materials):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.materials = materials  # 제작 재료템 시세 담은 리스트

        # 제작단 선택 콤보박스
        self.cb_production_team.activated[str].connect(self.change_production_team)

        # 제작 재료 테이블
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # 제작품 리스트 위젯
        self.listWidget_products.itemClicked.connect(self.change_cost)

    # 선택한 제작단 물품 보여주는 함수
    def change_production_team(self, production_team):
        self.listWidget_products.clear()
        select_production_team = f"SELECT 이름 FROM goods WHERE 제작단='{production_team}'"  # 선택한 제작단이 제작할 수 있는 제작품 불러오기
        cur.execute(select_production_team)
        rows = cur.fetchall()  # 선택한 제작단의 제작품 정보들을 담은 행
        for products_info in rows:
            self.listWidget_products.addItem(products_info[0])

    # 제작품 선택시 제작비 테이블 변경하고 총 제작비를 계산하는 함수
    def change_cost(self):
        self.product_name = self.listWidget_products.currentItem().text()
        column = 0
        self.materials_price = 0
        for materials_info in self.materials:   # self.materials는 {재료:가격}으로 구성된 딕셔너리들이 담긴 리스트
            material_name = list(materials_info.keys())[0] # 딕셔너리에서 키(재료이름)를 가져와서 저장
            material_price = materials_info[material_name]    # 가격 저장
            select_materials = f"SELECT {material_name} FROM goods WHERE 이름='{self.product_name}'"  # 제작에 필요한 재료의 개수 가져오기
            cur.execute(select_materials)
            materials_count = cur.fetchall()[0][0]
            all_price = round(materials_count * material_price)
            widget_item = [materials_count, material_price, all_price]    # 필요 개수, 현재 가격, 총 가격 (테이블 행 순으로 저장)
            # 테이블 갱신
            for row in range(3):
                item = QTableWidgetItem(str(widget_item[row]))
                self.tableWidget.setItem(row, column, item)
            column = column+1
            self.materials_price = self.materials_price + all_price # 재료값 합

        select_materials = f"SELECT 제작비 FROM goods WHERE 이름='{self.product_name}'"  # 제작품의 제작비(수수료) 가져오기
        cur.execute(select_materials)
        self.production_cost = cur.fetchall()[0][0] # 제작비(수수료)
        production_cost_str = '제작 수수료 : ' + str(self.production_cost) + '금'
        self.lbl_production_cost.setText(production_cost_str)


    #제작품 선택, 수수료 설정, 판매가격 설정시 총 제작비 및 수익 변경하는 함수
    # def calculate_cost(self):

if __name__ == '__main__':
    token = 'GPVLU=790E6C163B5AB2095E3D10D1F47ECCFD5FC185DC396F4245D1FCD20E91C8B4AB9BC6433C878DFA479EE36280A385335FB5F02FA5FAAD8927A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84DC1C97F11523EF5537555FD9C9DD32D9B32F4CC5436C602DC322FEB6F50FBA51443776F08B7CF1EDC3C7217473DFE47A5B90867DD2CB88E1400D2B054C5DBDB35BC3B06248B8CA0F4D6C59999C006BF2'
    cls_market = main.GetMarketInfo()
    materials = cls_market.get_material(token)

    app = QApplication(sys.argv)
    calcwindow = CalcWindow(materials)
    calcwindow.show()
    app.exec_()

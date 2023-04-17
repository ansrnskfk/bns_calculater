from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QDoubleValidator, QIcon
import sys
import pymysql
import getmarket

form_calcwindow = uic.loadUiType('calcwindow.ui')[0]

con = pymysql.connect(host='127.0.0.1', user='bns_db', password='336677', db='bns_calculater', charset='utf8')
cur = con.cursor()


class CalcWindow(QWidget, form_calcwindow):

    def __init__(self, materials, token):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.setWindowTitle('블소 계산기')
        self.materials = materials  # 제작 재료템 시세 담은 리스트
        self.token = token

        # 제작단 선택 콤보박스
        self.cb_production_team.activated[str].connect(self.change_production_team)

        # 제작품 리스트 위젯
        self.listWidget_products.itemClicked.connect(self.change_cost)

        # 제작 재료 테이블
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # 수수료 선택 콤보박스
        self.cb_charge.setDisabled(True)
        self.cb_charge.activated.connect(self.calculate_cost)

        # 판매 가격 설정 라디오 버튼, 라인에딧
        self.rb_lowest.setDisabled(True)
        self.rb_lowest.clicked.connect(self.clicked_rb_lowest)
        self.rb_direct.setDisabled(True)
        self.rb_direct.clicked.connect(self.clicked_rb_direct)
        self.le_price.setEnabled(False)
        self.le_price.setValidator(QDoubleValidator(self))
        self.le_price.textChanged.connect(self.calculate_cost)

    # 선택한 제작단 물품 보여주는 함수
    def change_production_team(self, production_team):
        self.listWidget_products.clear()
        select_production_team = f"SELECT 이름 FROM goods WHERE 제작단='{production_team}'"  # 선택한 제작단이 제작할 수 있는 제작품 불러오기
        cur.execute(select_production_team)
        rows = cur.fetchall()  # 선택한 제작단의 제작품 정보들을 담은 행
        for products_info in rows:
            self.listWidget_products.addItem(products_info[0])

    # 제작품 선택시 제작비 테이블 변경하고 총 제작비를 계산하는 함수
    # 제작품 선택 후 설정 관련 클릭제한 해제 및 시장 최저가 자동 입력
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
        production_cost_str = f'제작 수수료 : {str(self.production_cost)} 금'
        self.lbl_production_cost.setText(production_cost_str)

        self.cost = round(float((self.materials_price) + float(self.production_cost)))
        cost_str = f'총 제작비 : {str(self.cost)} 금'
        self.lbl_cost.setText(cost_str)

        self.cb_charge.setDisabled(False)
        self.rb_lowest.setDisabled(False)
        self.rb_direct.setDisabled(False)
        self.rb_lowest.setChecked(True)
        self.clicked_rb_lowest()

        self.calculate_cost()

    # 시장 최저가 버튼 선택후 가격 불러오기
    def clicked_rb_lowest(self):
        cls_market = getmarket.GetMarketInfo()
        get_product_price = cls_market.search_item(self.token, self.product_name)
        product_price = get_product_price[self.product_name]
        self.le_price.setText(str(product_price))
        self.le_price.setEnabled(False)

    # 가격 입력 제한 해제
    def clicked_rb_direct(self):
        self.le_price.setEnabled(True)

    #제작품 선택, 수수료 설정, 판매가격 설정시 묶음가격 및 수익 변경하는 함수
    def calculate_cost(self):
        select_product = f"SELECT 개수 FROM goods WHERE 이름='{self.product_name}'"  # 제작품의 개수 가져오기
        cur.execute(select_product)
        product_count = cur.fetchall()[0][0]  # 제작품의 개수
        product_count_str = f'{product_count}개 묶음 가격'
        self.lbl_product_count.setText(product_count_str)

        product_all_price = round(float(self.le_price.text()) * float(product_count))
        product_all_price_str = f'{product_all_price} 금'
        self.lbl_all_price.setText(product_all_price_str)

        price = float(product_all_price)
        cost = float(self.cost)
        charge = (100 - (self.cb_charge.currentIndex()+5)) / 100
        revenue = str(round(price * charge - cost))
        revenue_str = revenue + '금'
        self.lbl_revenue.setText(revenue_str)





if __name__ == '__main__':
    # token = 'GPVLU=790E6C163B5AB2095E3D10D1F47ECCFD5FC185DC396F4245D1FCD20E91C8B4AB9BC6433C878DFA479EE36280A385335FB5F02FA5FAAD8927A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84DC1C97F11523EF5537555FD9C9DD32D9B32F4CC5436C602DC322FEB6F50FBA51443776F08B7CF1EDC3C7217473DFE47A5B90867DD2CB88E1400D2B054C5DBDB35BC3B06248B8CA0F4D6C59999C006BF2'
    # cls_market = main.GetMarketInfo()
    # materials = cls_market.get_material(token)

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.png'))
    # calcwindow = CalcWindow(materials, token)
    # calcwindow.show()
    app.exec_()
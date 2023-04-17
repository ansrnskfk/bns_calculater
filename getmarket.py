from bs4 import BeautifulSoup
import re
import requests


class GetMarketInfo:

    # 제작 재료템 시세를 return 하는 함수
    def get_material(self, token):
        materials = []
        materials.append(self.search_item(token, '영석'))
        materials.append(self.search_item(token, '월석'))
        materials.append(self.search_item(token, '영단'))
        materials.append(self.search_item(token, '선단'))
        return materials

    # 아이템 시세 검색하고 return하는 함수
    def search_item(self, token, item):
        item_info = {}
        self.token = token
        self.item = item
        url = f"https://g-bnsmarket.plaync.com/bns/bidder/search.web?q={self.item}"
        headers = [
            {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'},
            {'Cookie': self.token}
        ]
        response = requests.get(url, headers=headers[1])
        soupBnsMarket = BeautifulSoup(response.content, 'html.parser')
        # print(soupBnsMarket)
        item_name = soupBnsMarket.find_all('span', attrs={'class': 'name noneAttribute'})  # 아이템 이름 추출
        name = item_name[0].string

        item_price = soupBnsMarket.find_all('dd', attrs={'class': 'price'})    # 아이템 가격 추출

        # 매물이 있는 경우와 없는 경우 구분
        if item_price:
            transgold = re.findall(r'\d+', re.sub(',', '', item_price[0].text)) # 숫자만 추출
            trans = 1
            price = 0
            for i in transgold:
                i = int(i)
                i = trans * i
                price = price + i
                trans = trans / 100
            item_info[name] = round(price, 2)
        else:
            item_info[name] = 0

        return item_info

    # 입력한 토큰이 정확한지 검증하는 함수
    def token_check(self, token):
        self.token = token
        url = "https://g-bnsmarket.plaync.com/bns/bidder/home.web"
        headers = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'},
            {'Cookie': self.token}
        ]
        response = requests.get(url, headers=headers[1])
        soupBnsMarket = BeautifulSoup(response.content, 'html.parser')
        item_name = soupBnsMarket.find_all('span', attrs={'class': 'name noneAttribute'})  # 아이템 이름 추출

        if item_name:
            return True
        else:
            return False


# g = GetMarketInfo()
# token = 'GPVLU=F245BEB7EE537FB626F3632DCAC6575DF0892381F2EFBFD6DC3E9EA553D0DEB7369C52549165827A9D79CA2DED75EE40FAD6191438F0A80FA54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84A54BBC1AD70B1A84D8AA3E3AEB81E36AFBD5102702FBB4FE515937D4B0218EC831D839400D4160956BA3BEAED19526C6933371B91336ED861A7076C131647A0D57F0E244A6DAB143676A671AD7BBFB63F506F21CBE8E1759'
# item = '월석'
# gm = g.getMarket(token, item)
# gc = g.token_check(token)
# print(gm)
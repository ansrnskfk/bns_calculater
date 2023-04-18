# bns_calculater

**exe파일 생성중 오류가 있어 현재 exe파일은 사용할 수 없습니다. 오류 해결 후 업데이트 예정입니다.**

## 1. 개발 배경
- 평소 즐겨하는 게임인 블레이드 앤 소울의 제작 시스템 개편 이후 수익을 얻을수 있게 됐다.
- 제작 아이템마다 수익이 다르고 시세가 매일 바뀌기 때문에 수익을 계산하고 싶었다.
- 엑셀로 정리해서 수익을 계산할 수 있었지만, 재료와 제작 아이템의 가격을 시장에서 확인하고 직접 수정해야 했기에 불편했다.
- 웹으로 볼 수 있는 시장에서 아이템의 가격을 크롤링 하면 가격을 직접 입력할 필요 없이 자동으로 수익을 계산할 수 있겠다고 생각한다.


## 2. 사용 방법
### 로그인 창

![Alt text](https://github.com/ansrnskfk/bns_calculater/blob/master/img/help1.jpg)
![Alt text](https://github.com/ansrnskfk/bns_calculater/blob/master/img/help2.png)

1. 블소 홈페이지 버튼을 눌러 로그인 합니다. 이때 웹 페이지는 열어놓습니다.
2. 웹 시장 버튼을 눌러 웹 시장에 접속합니다.
3. 웹 시장에서 f12(개발자 도구)를 누르고 / 네트워크 탭을 누르고 / Request Headers를 누른 뒤 / GPVLU=...로 된 부분을 **';'** 까지 포함해 복사 합니다.
4. 토큰 입력 칸에 붙여넣기 합니다.
5. 토큰 검증 버튼을 누르고 검증 성공 창이 뜨면
6. 로그인 버튼을 누릅니다.

### 계산기 창

![Alt text](https://github.com/ansrnskfk/bns_calculater/blob/master/img/calculater.png)

#### 1. 제작 물품
제작단을 선택할 수 있고 그 제작단의 제작품을 선택할 수 있습니다.

#### 2. 설정
판매 수수료와 판매 가격을 입력할 수 있습니다. 

#### 3. 제작 비용
제작에 필요한 재료의 개수와 가격, 제작 수수료와 이를 합한 총 제작비를 보여줍니다.

#### 4. 수익
최종 판매 수익을 보여줍니다.


## 3. 개발 과정

### 1. DB
- 제작품의 정보를 담을 DB가 필요했기에 MySQL을 사용해 DB를 만들었다.

![Alt text](https://github.com/ansrnskfk/bns_calculater/blob/master/img/DB.png)

### 2. PyQt5
- PyQt5 disigner로 GUI를 만들고 오브젝트들에 명령을 할당했다.

![Alt text](https://github.com/ansrnskfk/bns_calculater/blob/master/img/designer.png)
```python
# 사용 방법 버튼
self.btn_help.clicked.connect(self.open_helpwindow)

# 공홈 및 웹 시장 열기 버튼
self.btn_bns_web.clicked.connect(self.open_bns_url)
self.btn_market.clicked.connect(self.open_market_url)
...
...
```

### 3. pymysql
- DB를 파이썬 코드에서 사용하기 위해 pymysql 라이브러리를 사용했다.

```python
import pymysql
con = pymysql.connect(host='127.0.0.1', user='bns_db', password='비밀번호', db='bns_calculater', charset='utf8')
...
select_production_team = f"SELECT 이름 FROM goods WHERE 제작단='{production_team}'"  # 선택한 제작단이 제작할 수 있는 제작품 불러오기
...
```

### 4. BeautifulSoup
- 웹 시장에서 아이템의 가격을 크롤링 하기 위해 BeautifulSoup 및 request라이브러리를 사용했다.

```python
from bs4 import BeautifulSoup
import requests
...
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
    ...
```

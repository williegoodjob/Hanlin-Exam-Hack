#登入翰林速測
#看到題目後右鍵另存為"examine.html"
#將資料夾和examine.html移動到此檔案同層資料夾
#執行此腳本

#如報錯需檢查chromeDriver版本與chrome版本是否匹配

import atexit
from bs4 import BeautifulSoup
from selenium import webdriver
import shutil
import os

options = webdriver.ChromeOptions()
options.add_argument("--headless")                          #設置為無頭
driver = webdriver.Chrome('chromedriver', options=options)

id = []
Index = []
Indexdat = []
t = 1
map = ['A', 'B', 'C', 'D']
mapIndex = 0
file_path = ""

@atexit.register    #結束執行時關閉無頭chrome和刪除檔案
def web_close():
    driver.close()
    try:
        os.remove("examine.html")
    except OSError as e:
        print(e)
    else:
        print("File is deleted successfully")
    try:
        shutil.rmtree("examine_files")
    except OSError as e:
        print(e)
    else:
        print("The directory is deleted successfully")

def num(ch):        #判斷是否為數字
    if '1' <= ch <= '4':
        return 1
    return 0

with open(file_path + "examine.html", "r", encoding="utf-8") as fp:
    soup = BeautifulSoup(fp, "html.parser")                         #開啟文件
    a_tags = soup.find_all('input', {'name': 'actionQuestionNum'})  #在文件中尋找包含js檔名的html
    for tag in a_tags:
        id.extend([tag.get('question')])                #取得js檔名的html
    for x in range(len(id)):                            #for迴圈直到沒有題目
        str = "view-source:https://d1ocvtypb16jkr.cloudfront.net/v1/items/" + \
              id[x] + "/assets/frameHtml/question.html?v=0.2.5&bucket=itembank&source=cf&t=1625099422272"       #組合js腳本的url
        # print(str)
        driver.get(str)                                             #在chrome中移動到網址
        soup1 = BeautifulSoup(driver.page_source, 'html.parser')    #取得網頁原始碼
        soup1.find_all('td', {'class': 'line-content'})             #分離內文
        s = soup1.text                                              #將內文存入s變數
        ix = s.find('"answer"', 3000)                               #從3000字以後尋找"answer"
        while ix != -1:                                             #如果找到(返回不等於-1)
            Index.extend([ix])                                      #把找到的索引存到Index陣列
            ix = s.find('"answer"', ix + 1)
        for n in range(len(Index)):                                 #重複"答案數"次(理論只有一次
            if num(s[Index[n] + 13]):                               #擷取答案索引(1~4)並判斷是否為數字
                Indexdat.extend(s[Index[n] + 13])                   #把答案索引存入Indexdat陣列
        for n in range(len(Indexdat)):                              #重複"答案數"次(理論只有一次
            mapIndex = int(Indexdat[n])                             #將陣列轉型為整數
            Indexdat[n] = map[mapIndex - 1]                         #把答案陣列的索引(1~4)換成答案(A~D)，由於索引資料是1~4，而陣列索引是0~4，因此需減1
        # Indexdat[4] = t
        print(t, Indexdat)                                          #顯示題號和答案
        print()                                                     #插入一行空白
        t = t + 1                                                   #題號+1
        del Index[:]                                                #清空陣列以備下次掃描
        del Indexdat[:]                                             #清空陣列以備下次掃描

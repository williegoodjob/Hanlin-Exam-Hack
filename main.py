import atexit
from bs4 import BeautifulSoup
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome('chromedriver', options=options)
# driver.minimize_window()
id = []
Index = []
Indexdat = []
t = 1
map = ['A', 'B', 'C', 'D']
mapIndex = 0


@atexit.register
def web_close():
    driver.close()


def num(ch):
    if '1' <= ch <= '4':
        return 1
    return 0




with open("examine.html", "r", encoding="utf-8") as fp:
    soup = BeautifulSoup(fp, "html.parser")
    a_tags = soup.find_all('input', {'name': 'actionQuestionNum'})
    for tag in a_tags:
        id.extend([tag.get('question')])
    for x in range(len(id)):
        str = "view-source:https://d1ocvtypb16jkr.cloudfront.net/v1/items/" + id[
            x] + "/assets/frameHtml/question.html?v=0.2.5&bucket=itembank&source=cf&t=1625099422272"
        # print(str)
        driver.get(str)
        soup1 = BeautifulSoup(driver.page_source, 'html.parser')
        soup1.find_all('td', {'class': 'line-content'})
        s = soup1.text
        ix = s.find('"answer"', 3000)
        while ix != -1:
            Index.extend([ix])
            ix = s.find('"answer"', ix + 1)
        for n in range(len(Index)):
            if num(s[Index[n]+13]):
                Indexdat.extend(s[Index[n] + 13])
        for n in range(len(Indexdat)):
            mapIndex = int(Indexdat[n])
            Indexdat[n] = map[mapIndex - 1]
        # Indexdat[4] = t
        print(t, Indexdat)
        print()
        t = t + 1
        del Index[:]
        del Indexdat[:]

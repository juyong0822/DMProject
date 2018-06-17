from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
import time
from konlpy.tag import Twitter

t = Twitter()

driver = webdriver.Chrome('C:\\Users\\juyon\\chromedriver.exe')

saveloc = "..\\Crawling"
savetextloc = saveloc + "Files0617\\"
savehtmlloc = saveloc + "Htmls0617\\"
last_sentences = []
last_sentences_html = []

baseurl = 'http://glaw.scourt.go.kr/wsjo/panre/sjo100.do?saNo='

search = {'도로교통법': 41, '교통사고 처리 특례법': 16}


def get_3sentences(keyword, fail, success):

    for sent in last_sentences:
        nodata2 = False
        nodata1 = False
        print('fail :', fail, 'success :', success)
        print(sent)
        driver.get(baseurl + sent)
        time.sleep(1)
        html3 = driver.page_source
        soup3 = BeautifulSoup(html3, 'html.parser')   # BeautifulSoup사용하기
        strong3 = soup3.find_all('strong')

        for st in strong3:
            if st.get('id') == 'SubjectDecision':
                if len(st.select('a')) is 0:
                    nodata2 = True
                    break
                driver.get(baseurl + st.select('a')[0].get('type').split('|')[1])
                break

        if nodata2:
            print('nodata2 fail')
            fail += 1
            continue

        time.sleep(1)
        print('check last sentence')

        try:
            alert = driver.switch_to.alert
            alert.accept()
            print('nodata2 fail')
            fail += 1
            continue
        except NoAlertPresentException:
            pass

        html2 = driver.page_source
        soup2 = BeautifulSoup(html2, 'html.parser')
        strong2 = soup2.find_all('strong')

        for st in strong2:
            if st.get('id') == 'SubjectDecision':
                if len(st.select('a')) is 0:
                    nodata1 = True
                    break
                driver.get(baseurl + st.select('a')[0].get('type').split('|')[1])
                break

        if nodata1:
            print('nodata1 fail')
            fail += 1
            continue

        time.sleep(1)
        print('check 2nd sentence')

        try:
            alert = driver.switch_to.alert
            alert.accept()
            print('fail')
            fail += 1
            continue
        except NoAlertPresentException:
            pass

        html1 = driver.page_source
        soup1 = BeautifulSoup(html1, 'html.parser')

        if soup2.find("div", {"class": "page_area"}) is None or soup1.find("div", {"class": "page_area"}) is None:
            print('?????? fail')
            fail += 1
            continue

        text3 = soup3.find("div", {"class": "page_area"}).get_text()
        text2 = soup2.find("div", {"class": "page_area"}).get_text()
        text1 = soup1.find("div", {"class": "page_area"}).get_text()
        success += 1

        savetext(keyword, text3, text2, text1, success)
        savehtml(keyword, html3, html2, html1, success)


def savetext(keyword, text3, text2, text1, success):
    f3 = open(savetextloc + keyword + '_' + str(success) + '_3.txt', 'w', encoding="UTF-8")
    f3.write(text3)
    f3.close()
    f2 = open(savetextloc + keyword + '_' + str(success) + '_2.txt', 'w', encoding="UTF-8")
    f2.write(text2)
    f2.close()
    f1 = open(savetextloc + keyword + '_' + str(success) + '_1.txt', 'w', encoding="UTF-8")
    f1.write(text1)
    f1.close()


def savehtml(keyword, html3, html2, html1, success):
    f3 = open(savehtmlloc + keyword + '_' + str(success) + '_3.txt', 'w', encoding="UTF-8")
    f3.write(html3)
    f3.close()
    f2 = open(savehtmlloc + keyword + '_' + str(success) + '_2.txt', 'w', encoding="UTF-8")
    f2.write(html2)
    f2.close()
    f1 = open(savehtmlloc + keyword + '_' + str(success) + '_1.txt', 'w', encoding="UTF-8")
    f1.write(html1)
    f1.close()


def get_sentences(keyword, pages):
    for i in range(pages):
        driver.get('http://glaw.scourt.go.kr/wsjo/panre/sjo050.do?q=' + keyword + '&pg='+str(i+1))
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        trs = soup.find_all('tr')

        for tr in trs[1:]:
            tr = t.morphs(tr.get_text())
            i = 0
            for token in tr:
                if token == '선고' or token == '자':
                    e = tr[i + 1] + tr[i + 2] + tr[i + 3]
                    break
                i += 1
            last_sentences.append(e)
    get_3sentences(keyword, fail=0, success=0)


for key, pages in search.items():
    get_sentences('상고 ' + key, pages)

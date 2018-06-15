from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
import time
from konlpy.tag import Twitter
import selenium
import requests

t = Twitter()

driver = webdriver.Chrome('C:\\Users\\juyon\\chromedriver.exe')
# driver = webdriver.PhantomJS('C:\\Users\\juyon\\phantomjs-2.1.1-windows\\bin\\phantomjs')

pages_htmls = []

last_sentences = []
second_sentences = []
first_sentences = []

last_sentences_html = []
second_sentences_html = []
first_sentences_html = []

baseurl = 'http://glaw.scourt.go.kr/wsjo/panre/sjo100.do?saNo='
num = 1
pages = 1           # 39 pages

fail = 0
success = 0

def get_sentences(pages):
    for i in range(pages):
        driver.get('http://glaw.scourt.go.kr/wsjo/panre/sjo050.do?q=%EC%83%81%EA%B3%A0%20%EB%8F%84%EB%A1%9C%EA%B5%90%ED%86%B5%EB%B2%95&pg='+str(i+1))
        time.sleep(1)
        pages_htmls.append(driver.page_source)

    for html in pages_htmls:
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


def get_3sentences():
    global fail
    global success
    for sent in last_sentences:
        driver.get(baseurl + sent)
        time.sleep(1)
        last_sentences_html.append(driver.page_source)  # 페이지의 elements모두 가져오기

    i = 0

    for html3 in last_sentences_html:
        i += 1
        print(i)
        soup3 = BeautifulSoup(html3, 'html.parser')   # BeautifulSoup사용하기
        strong3 = soup3.find_all('strong')

        for st in strong3 :
            if st.get('id') == 'SubjectDecision':
                driver.get(baseurl + st.select('a')[0].get('type').split('|')[1])

        time.sleep(1)
        print('check last sentence')

        try:
            alert = driver.switch_to.alert
            alert.accept()
            print('fail')
            fail += 1
            continue
        except NoAlertPresentException:
            pass

        html2 = driver.page_source
        soup2 = BeautifulSoup(html2, 'html.parser')
        strong2 = soup2.find_all('strong')

        for st in strong2 :
            if st.get('id') == 'SubjectDecision':
                driver.get(baseurl + st.select('a')[0].get('type').split('|')[1])

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
        print(soup1.find("div", {"class":"page_area"}).get_text())
        success += 1





get_sentences(pages)
print(last_sentences)
get_3sentences()

"""
for sent in sentence :
    # driver.get('https://www.google.com')
    driver.get('http://glaw.scourt.go.kr/wsjo/panre/sjo100.do?saNo=' + sent)
    time.sleep(1)
    htmls.append(driver.page_source)    # 페이지의 elements모두 가져오기

a =
"""
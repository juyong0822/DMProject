# -*- coding: utf-8 -*-

import io
from bs4 import BeautifulSoup
from konlpy.tag import Komoran
import nltk

location = "..\\CrawlingHtmls0617_2\\"

doc_num = 1048
keyword = {'손해배상': doc_num}

stopwords = ['이', '있', '하', '것', '들', '그', '되', '수', '보', '나', '다', '사람', '주', '거',
             '호', '년', '월', '일', '가', '의', '를', '하다', '함', '오', '때', '한', '더', '그것',
             '대한', '그런', '또', '더', '중', '씨', '하나', '적', '데', '내', '어떤', '이런', '다시',
             '번', '경우', '제', '조', '항', '개', '갑', '을', '병', '정', '점', '원', '정도', '이하',
             '하는', '각', '서', '만', '아래', '같은', '‘', '’', '하', 'ㄴ', '이', '아', '는', '고',
             '제', '있', '되', '년', '월', '일', '가', '다', 'ㄹ', '았', '위', '공', '것', '어', '제',
             '호', '조', '항', '등', '그', '대하', '지', '수', '은', '들', '었', '원', '및', '에서',
             '라고', '다음', '.', ',', '에', '부터', '로부터', '해', '생략', ':', '(', ')', '세', '미터',
             '간', '으로', '뒷', '서림', '종합', '①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨']

komoran = Komoran()

accept = [0] * doc_num
# add_words = ['항소', '이유', '형', '판례', '검사', '사건', '요지', '피고인', '사실']
# for w in add_words:
#    stopwords.append(w)

def generate_docs1():
    global stopwords
    docs = []
    for key, value in keyword.items():
        for i in range(value):
            print(i)
            file_name2 = location + '상고 ' + key + '_' + str(i+1) + '_2.txt'
            file_name3 = location + '상고 ' + key + '_' + str(i+1) + '_3.txt'
            f2 = io.open(file_name2, mode='r', encoding='utf-8')
            html2 = f2.read()
            f2.close()
            f3 = io.open(file_name3, mode='r', encoding='utf-8')
            html3 = f3.read()
            f3.close()

            soup2 = BeautifulSoup(html2, 'html.parser')  # BeautifulSoup사용하기
            p2 = soup2.find_all('p')

            j = 0
            reason2 = ''
            for p in p2:
                if len(p.select('strong')) > 0:
                    if p.select('strong')[0].get('id') == 'Reason':
                        for k in range(j+1, len(p2)):
                            reason2 += p2[k].get_text()
                        break
                j += 1

            soup3 = BeautifulSoup(html3, 'html.parser')  # BeautifulSoup사용하기
            p3 = soup3.find_all('p')

            j = 0
            outcome3 = ''
            for p in p3:
                if len(p.select('strong')) > 0:
                    if p.select('strong')[0].get('id') == 'OutCome':
                        outcome3 = p3[j+1].get_text()
                        break
                j += 1

            outcome3 = komoran.morphs(outcome3)
            reason2_pos = komoran.pos(reason2)

            if '기각' in outcome3:
                accept[i] = False
            else: accept[i] = True

            reason2 = []
            print(reason2_pos)

            for word, pos in reason2_pos:
                if pos[0] != 'S' and word not in stopwords:
                    reason2.append(word)
            docs.append(reason2)
            print(reason2)
    return docs


wordlist = []
for doc in generate_docs1():
    for word in doc:
        wordlist.append(word)

ko = nltk.Text(wordlist)

print(ko.vocab().most_common(ko.vocab().B()))
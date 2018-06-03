import io
from konlpy.tag import Twitter

keyword = {'상고 교통법 1항' : 7 , '상고 교통법 2항' : 8, '상고 교통법 3항' : 8, '상고 도로교통법' : 9,
            '상고 교통사고' : 7, '상고 교통법' : 11, '상고 교통법 운전자' : 7, '상고 교통사고 특례' : 9,
            '상고 뺑소니' : 5, '상고 교통법 신호' : 9}

t = Twitter()

for key, value in keyword.items() :
    for i in range(value):
        file_name = u'..\\CrawlingFiles\\'+key+'_'+str(i)+'_1.txt'
        f = io.open(file_name, mode = 'r', encoding = 'utf-8')
        read_file = f.read()
        f.close()                           # for문 한번 돌 때마다 파일 하나 읽어옴

        tokens = t.morphs(read_file)        # 읽은 파일 토큰화해서 리스트로 정리
        print(tokens)
import io
from konlpy.tag import Twitter

keyword = {'상고 교통법 1항' : 7 , '상고 교통법 2항' : 8, '상고 교통법 3항' : 8, '상고 도로교통법' : 9,
            '상고 교통사고' : 7, '상고 교통법' : 11, '상고 교통법 운전자' : 7, '상고 교통사고 특례' : 9,
            '상고 뺑소니' : 5, '상고 교통법 신호' : 9}

t = Twitter()
k = 0
for key, value in keyword.items() :
    for i in range(value):
        file_name = u'..\\CrawlingFiles\\'+key+'_'+str(i)+'_1.txt'
        f = io.open(file_name, mode = 'r', encoding = 'utf-8')
        read_file = f.read()
        f.close()                           # for문 한번 돌 때마다 파일 하나 읽어옴

        print(read_file)                    # 읽어온 파일(string)

        doc = read_file[read_file.index("가입") + 3 : len(read_file)-155]       # 쓸데없는 단어들 제거(로그인, 회원가입 등)

        print(doc)

        print(k, t.pos(doc))                   # 포스 태깅 완료(list)
        k += 1
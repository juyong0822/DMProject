from konlpy.tag import Komoran, Twitter

k = Komoran()
t = Twitter()

st = '민사소송법 제420조 본문을 그대로 인용한다.'

print(k.pos(st))
print(t.pos(st))

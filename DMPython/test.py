
from konlpy.tag import Twitter

t = Twitter()

a = "대법원 1994. 10. 7. 자 94도2172 판결"
a = t.morphs(a)

i = 0
for token in a :
    if token == '선고' or token == '자':
        e = a[i+1] + a[i+2] + a[i+3]
        break
    i += 1
print(e)
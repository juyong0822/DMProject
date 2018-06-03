import io
import time
from gensim.models.doc2vec import TaggedDocument,Doc2Vec
from konlpy.tag import Twitter


keyword = {'상고 교통법 1항' : 7 , '상고 교통법 2항' : 8, '상고 교통법 3항' : 8, '상고 도로교통법' : 9,
            '상고 교통사고' : 7, '상고 교통법' : 11, '상고 교통법 운전자' : 7, '상고 교통사고 특례' : 9,
            '상고 뺑소니' : 5, '상고 교통법 신호' : 9}

t = Twitter()

doc_vectorizer = Doc2Vec(
    dm=0,            # PV-DBOW / default 1
    dbow_words=1,    # w2v simultaneous with DBOW d2v / default 0
    window=8,        # distance between the predicted word and context words
    vector_size=300,        # vector size
    alpha=0.025,     # learning-rate
    seed=1234,
    min_count=20,    # ignore with freq lower
    min_alpha=0.025, # min learning-rate
    workers=4,   # multi cpu
    hs = 1,          # hierarchical softmax / default 0
    negative = 10,   # negative sampling / default 5
)

docs = []

for key, value in keyword.items() :
    for i in range(value):
        file_name = u'../CrawlingFiles/'+key+'_'+str(i)+'_1.txt'
        f = io.open(file_name, mode = 'r', encoding = 'utf-8')
        read_file = f.read()
        f.close()                           # for문 한번 돌 때마다 파일 하나 읽어옴

        doc = read_file[read_file.index("가입") + 3: len(read_file) - 155]  # 쓸데없는 단어들 제거(로그인, 회원가입 등)

        # taggedDoc = t.pos(doc)  # 포스 태깅 완료(list)

        T = TaggedDocument(t.morphs(doc), [key + '_' + str(i) + '_1'])

        docs.append(T)

doc_vectorizer.build_vocab(docs)

start = time.time()
for epoch in range(doc_vectorizer.iter):
    doc_vectorizer.train(docs, total_examples=doc_vectorizer.corpus_count, epochs=doc_vectorizer.iter)
    doc_vectorizer.alpha -= 0.002 # decrease the learning rate
    doc_vectorizer.min_alpha = doc_vectorizer.alpha # fix the learning rate, no decay
    print(epoch)
end = time.time()
print("During Time: {}".format(end-start))
model_name = str(doc_vectorizer) + '.model'
doc_vectorizer.save(model_name)

for i in range(100):
    print(i, doc_vectorizer.docvecs[i])

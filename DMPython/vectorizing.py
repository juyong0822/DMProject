import time
from gensim.models.doc2vec import Doc2Vec
import math

keyword = {'상고 도로교통법' : 9, '상고 교통사고' : 7, '상고 교통법' : 11, '상고 교통법 운전자' : 7,
           '상고 교통사고 특례' : 9, '상고 뺑소니' : 5, '상고 교통법 신호' : 9, '상고 교통법 1항' : 7 ,
           '상고 교통법 2항' : 8, '상고 교통법 3항' : 8, '상고 교통법 4항' : 5, '상고 교통법 5항' : 3,
           '상고 교통법 6항' : 2, '상고 교통법 7항' : 1, '상고 교통법 재' : 18, '상고 교통법 학교' : 18,
           '상고 교통법 지역' : 16, '상고 교통법 장소' : 11, '상고 교통법 건물' : 9, '상고 교통법 보행자' : 6,
           '상고 교통법 위반' : 13, '상고 교통법 벌금' : 15, '상고 교통법 사망' : 11, '상고 교통법 보험' : 22
           }

doc_vectorizer = Doc2Vec(
    dm=0,            # PV-DBOW / default 1
    dbow_words=1,    # w2v simultaneous with DBOW d2v / default 0
    window=8,        # distance between the predicted word and context words
    vector_size=1000,        # vector size
    alpha=0.025,     # learning-rate
    seed=1234,
    min_count=20,    # ignore with freq lower
    min_alpha=0.025, # min learning-rate
    workers=4,   # multi cpu
    hs = 1,          # hierarchical softmax / default 0
    negative = 10,   # negative sampling / default 5
)


def cos_similarity(vec1, vec2):
    vec1_sumsq = 0
    for i in range(vec1.size):
        vec1_sumsq += vec1[i] ** 2
    vec1_size = math.sqrt(vec1_sumsq)

    vec2_sumsq = 0
    for i in range(vec2.size):
        vec2_sumsq += vec2[i] ** 2
    vec2_size = math.sqrt(vec2_sumsq)

    vecProd = 0
    for i in range(vec1.size):
        vecProd += vec1[i] * vec2[i]

    return vecProd / (vec1_size * vec2_size)


def generate_docs1():
    pass        # generate docs to word list


start = time.time()
docs = generate_docs1()
doc_vectorizer.build_vocab(docs)
end = time.time()
print("During Time: {}".format(end-start))

start = time.time()
for epoch in range(doc_vectorizer.iter):
    doc_vectorizer.train(docs, total_examples=doc_vectorizer.corpus_count, epochs=doc_vectorizer.iter)
    doc_vectorizer.alpha -= 0.002 # decrease the learning rate
    doc_vectorizer.min_alpha = doc_vectorizer.alpha # fix the learning rate, no decay
end = time.time()
print("During Time: {}".format(end-start))

# for i in range(100):
#    print(i, doc_vectorizer.docvecs[i])

print(str(len(docs)) + "개 문서")

"""

i, j = 58, 59
print(docs[i])
print(docs[j])
print(cos_similarity(doc_vectorizer.docvecs[i], doc_vectorizer.docvecs[j]))

i, j = 58, 100
print(docs[i])
print(docs[j])
print(cos_similarity(doc_vectorizer.docvecs[i], doc_vectorizer.docvecs[j]))

i, j = 80, 100
print(docs[i])
print(docs[j])
print(cos_similarity(doc_vectorizer.docvecs[i], doc_vectorizer.docvecs[j]))

"""
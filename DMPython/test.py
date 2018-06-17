import io
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from bs4 import BeautifulSoup
import time
from konlpy.tag import Twitter
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

location = "..\\CrawlingHtmls0617_2\\"

keyword = {'도로교통법': 105}

t = Twitter()

stopwords = ['이', '있', '하', '것', '들', '그', '되', '수', '보', '나', '다', '사람', '주', '거',
             '호', '년', '월', '일', '가', '의', '를', '하다', '함', '오', '때', '한', '더', '그것',
             '대한', '그런', '또', '더', '중', '씨', '하나', '적', '데', '내', '어떤', '이런', '다시',
             '번', '경우', '제', '조', '항', '개', '갑', '을', '병', '정', '점', '원', '정도', '이하',
             '하는', '각', '서', '만', '아래', '같은', '‘', '’']

accept = [0] * 105
# add_words = ['항소', '이유', '형', '판례', '검사', '사건', '요지', '피고인', '사실']
# for w in add_words:
#    stopwords.append(w)

def generate_docs1():
    global stopwords
    docs = []
    for key, value in keyword.items() :
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

            outcome3 = t.morphs(outcome3)
            reason2_pos = t.pos(reason2)

            if '기각' in outcome3:
                accept[i] = False
            else: accept[i] = True

            reason2 = []

            for j in range(len(reason2_pos)):
                (word, pos) = reason2_pos[j]
                if word not in stopwords and pos != 'Number' and pos != 'Punctuation' and pos != 'Josa':
                    reason2.append(word)
            docs.append(reason2)
            print(reason2)
    return docs


word_pos = {}
word_neg = {}
word_sentiment = {}

docs = generate_docs1()

for i in range(105):
    for doc in docs:
        if accept[i]:
            for w in doc:
                if w not in word_pos:
                    word_pos[w] = 1
                else:
                    word_pos[w] += 1
        else:
            for w in doc:
                if w not in word_neg:
                    word_neg[w] = 1
                else:
                    word_neg[w] += 1

print(word_pos)
print(word_neg)

"""

doclist = []
for i in range(len(docs)):
    doclist.append(TaggedDocument(docs[i], ['상고 도로교통법_' + str(i)]))

doc_vectorizer = Doc2Vec(
    # dm=0,            # PV-DBOW / default 1
    # dbow_words=1,    # w2v simultaneous with DBOW d2v / default 0
    # vector_size=300,        # vector size
    window=8,        # distance between the predicted word and context words
    alpha=0.025,     # learning-rate
    seed=1234,
    min_count=20,    # ignore with freq lower
    min_alpha=0.025, # min learning-rate
    workers=4,   # multi cpu
    hs=1,          # hierarchical softmax / default 0
    negative=10,   # negative sampling / default 5
)

start = time.time()
doc_vectorizer.build_vocab(doclist)
for epoch in range(doc_vectorizer.iter):
    doc_vectorizer.train(doclist, total_examples=doc_vectorizer.corpus_count, epochs=doc_vectorizer.iter)
    doc_vectorizer.alpha -= 0.002 # decrease the learning rate
    doc_vectorizer.min_alpha = doc_vectorizer.alpha # fix the learning rate, no decay
end = time.time()
print("During Time: {}".format(end-start))

doc_vectors = []
doc_vectors_accept = []

for i in range(len(doclist)):
    doc_vectors.append(doc_vectorizer.docvecs[i])
    if accept[i]:
        doc_vectors_accept.append(1)
    else:
        doc_vectors_accept.append(0)

print(doc_vectors)
print(doc_vectors_accept)


x_train = doc_vectors[0:80]
x_test = doc_vectors[80:105]
y_train = doc_vectors_accept[0:80]
y_test = doc_vectors_accept[80:105]
x_train = np.array(x_train)
x_test = np.array(x_test)
y_train = np.array(y_train)
y_test = np.array(y_test)

# SVM Classifier
svm_clf = Pipeline([('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=   5, random_state=42)),])
# fit svm model to classify training set
svm_clf.fit(x_train, y_train)
# dump the job to file

predicted = svm_clf.predict(x_test)
print('SVM correct prediction: {:4.2f}'.format(np.mean(predicted == y_test)))
print(predicted)

# print(metrics.classification_report(y_test, predicted, target_names=[0,1]))

# print(metrics.confusion_matrix(y_test, predicted))


# tokenise new doc
# from konlpy.tag import Twitter
# unclassifieddoc =

# vectorise new doc
# def getVecs(model, corpus, size):
#     vecs = [np.array(model[z.labels[0]]).reshape((1, size)) for z in corpus]
#     return np.concatenate(vecs)

# unclassifiedvec = getVecs(doc_vectorizer, unclassifieddoc, vector_size=300)

# print prediction using SVM
# print(svm_clf.predict(unclassifiedvec))

"""
import gensim
import os

LabeledSentence = gensim.models.doc2vec.LabeledSentence

from sklearn.cross_validation import train_test_split
import numpy as np

with open('IMDB_data/pos.txt','r') as infile:
    pos_reviews = infile.readlines()

with open('IMDB_data/neg.txt','r') as infile:
    neg_reviews = infile.readlines()

with open('IMDB_data/unsup.txt','r') as infile:
    unsup_reviews = infile.readlines()

#use 1 for positive sentiment, 0 for negative
y = np.concatenate((np.ones(len(pos_reviews)), np.zeros(len(neg_reviews))))

#splitting into 80/20,                                  join both up                        y corresponds to p/n
x_train, x_test, y_train, y_test = train_test_split(np.concatenate((pos_reviews, neg_reviews)), y, test_size=0.2)
#x splitting also indexed by y
#Do some very minor text preprocessing
def cleanText(corpus):
    punctuation = """.,?!:;(){}[]"""
    corpus = [z.lower().replace('\n','') for z in corpus]
    corpus = [z.replace('<br />', ' ') for z in corpus]

    #treat punctuation as individual words
    for c in punctuation:
        corpus = [z.replace(c, ' %s '%c) for z in corpus]
    corpus = [z.split() for z in corpus]
    return corpus

x_train = cleanText(x_train)
x_test = cleanText(x_test)
unsup_reviews = cleanText(unsup_reviews)

#Gensim's Doc2Vec implementation requires each document/paragraph to have a label associated with it.
#We do this by using the LabeledSentence method. The format will be "TRAIN_i" or "TEST_i" where "i" is
#a dummy index of the review.
def labelizeReviews(reviews, label_type):
    labelized = []
    for i,v in enumerate(reviews):
        label = '%s_%s'%(label_type,i)
        labelized.append(LabeledSentence(v, [label]))
    return labelized

x_train = labelizeReviews(x_train, 'TRAIN')
x_test = labelizeReviews(x_test, 'TEST')
unsup_reviews = labelizeReviews(unsup_reviews, 'UNSUP')




#just require string(array) of all from positive 1 joined with 2 +  negative 1 and 2 and the unsup


#START HERE




import random

size = 400

#instantiate our DM and DBOW models
model_dm = gensim.models.Doc2Vec(min_count=1, window=10, size=size, sample=1e-3, negative=5, workers=3)
model_dbow = gensim.models.Doc2Vec(min_count=1, window=10, size=size, sample=1e-3, negative=5, dm=0, workers=3)
#min_count: ignore all words with frequency lower than this
#window: max dist between current and predicted word within a sentence
#size: dimension of feature vector
#sample: threshold for configuring with high freq word
#negative: how many noise words should be drawn
#workers: thread to train model


#build vocab over all reviews (built by XXX)
model_dm.build_vocab(np.concatenate((x_train, x_test, unsup_reviews)))
model_dbow.build_vocab(np.concatenate((x_train, x_test, unsup_reviews)))

#We pass through the data set multiple times, shuffling the training reviews each time to improve accuracy.
all_train_reviews = np.concatenate((x_train, unsup_reviews))
for epoch in range(10):
    perm = np.random.permutation(all_train_reviews.shape[0])
    model_dm.train(all_train_reviews[perm])
    model_dbow.train(all_train_reviews[perm])



#Get training set vectors from our models
def getVecs(model, corpus, size):
    vecs = [np.array(model[z.labels[0]]).reshape((1, size)) for z in corpus]
    return np.concatenate(vecs)

train_vecs_dm = getVecs(model_dm, x_train, size)
train_vecs_dbow = getVecs(model_dbow, x_train, size)

#stack horizontally
train_vecs = np.hstack((train_vecs_dm, train_vecs_dbow))

#train over test set
x_test = np.array(x_test)

for epoch in range(10):
    perm = np.random.permutation(x_test.shape[0])
    model_dm.train(x_test[perm])
    model_dbow.train(x_test[perm])

#Construct vectors for test reviews
test_vecs_dm = getVecs(model_dm, x_test, size)
test_vecs_dbow = getVecs(model_dbow, x_test, size)

test_vecs = np.hstack((test_vecs_dm, test_vecs_dbow))#concentate

#If you look at the results (cell 12) of the notebook, you'll see that the combination that the original paper implies does best, PV-DBOW doc-vectors concatenated
#with PV-DM-with-a-concatenative-input-layer (`dbow+dmc` in the notebook's naming), does no better than PV-DBOW alone.
#Another concatenated-combination of two models' doc-vectors, `dbow+dmm`, does a teensy smidge better than PV-DBOW (0.00108 lower error rate) – but that probably isn't significant, given the jitter in error rates from run to run.

#Now we are ready to train a classifier over our review vectors. We will again use sklearn's SGDClassifier.



from sklearn.linear_model import SGDClassifier

lr = SGDClassifier(loss='log', penalty='l1')
lr.fit(train_vecs, y_train)

#test against y_test whether 1 or 2
print ('Test Accuracy: %.2f'%lr.score(test_vecs, y_test))

import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

doc_vectors = []
doc_vectors_accept = []

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

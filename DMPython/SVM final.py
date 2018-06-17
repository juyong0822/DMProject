# Assume data set is split into 80/20
# x_train, x_test, y_train, y_test = train_test_split(np.concatenate((pos_reviews, neg_reviews)), y, test_size=0.2)
# x_train vectors matched with y_train 80
# x_test vectors matched with y_test 20
# y_train and y_test is vector [0,1,1,1,0,0....0] (y is the positive negative)

# SVM requires  2 list of vectors ((x_train)1 list of vectors for documents used in training(600)
# and (x_test)another list of vectors for documents used in testing(200))
# and 2 more corresponding list( (y_train)1 list for training(600) to indicate
# 0=appeal fail and 1=appeal pass and (y_test) another list for testing(200) for
# 0=appeal fail and 1= appeal pass)

# change list to np.array



#SVM Classifier
svm_clf = Pipeline([
    ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=   5, random_state=42)),
])
#fit svm model to classify training set 
svm_clf.fit(x_train,x_target)
#dump the job to file
joblib.dump(svm_clf, "svm_.pkl", compress=9)

predicted = svm_clf.predict(x_test)
print('SVM correct prediction: {:4.2f}'.format(np.mean(predicted == y_test)))
print(metrics.classification_report(y_test, predicted, target_names=[0,1]))

print(metrics.confusion_matrix(y_test, predicted))


#tokenise new doc
#from konlpy.tag import Twitter
#unclassifieddoc =

#vectorise new doc
#def getVecs(model, corpus, size):
#    vecs = [np.array(model[z.labels[0]]).reshape((1, size)) for z in corpus]
#    return np.concatenate(vecs)

#unclassifiedvec = getVecs(doc_vectorizer, unclassifieddoc, vector_size=300)

#print prediction using SVM
#print(svm_clf.predict(unclassifiedvec))

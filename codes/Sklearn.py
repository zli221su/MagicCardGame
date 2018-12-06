from sklearn import svm
from training_set_X import *
from training_set_Y import *

clf = svm.SVR(kernel = 'linear')

clf.fit(X, Y)

##pred = clf.predict(X)

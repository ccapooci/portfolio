# Import Basic Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import Sklearn
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix

# Prints optimal values for inputted parameters along w/ classification report
# Inputs :
# - paramGrid : parameters to cycle through for optimal value
# - k : Kernal type for grid search
def Grid(paramGrid, k , x_train, x_test, y_train, y_test):
    grid = GridSearchCV(SVC(kernel=k), paramGrid, cv=5)
    grid.fit(x_train, y_train.values.ravel())
    predict = grid.predict(x_test)

    # Print
    print('\n'+ k+' best parameters:')
    print(grid.best_params_)
    print(classification_report(y_test,predict))

#------Main------

# import data
df = pd.read_csv('svm_2022/svm_data_2022.csv')

# prints answer for a
print(df['Class'].value_counts())

# stratify and split data
y = df.pop('Class').to_frame()
x = df
x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y, test_size=0.8)

# print result for b
print('testing set')
print(y_test.value_counts())
print('training set')
print(y_train.value_counts())

# import testing and training data
dftest = pd.read_csv('svm_2022/test_data_2022.csv')
dftrain = pd.read_csv('svm_2022/train_data_2022.csv')

# reset test and train vals to requested values
y_train = dftrain.pop('Class').to_frame()
y_test = dftest.pop('Class').to_frame()
x_train = dftrain
x_test = dftest

# Apply svc
C = np.array([0.1, 0.2, 0.3, 0.5, 1, 2, 3, 5, 10])
supportVectors = []
for i in C:
    clf = SVC(C=i,kernel='linear') # Update SVC to new C
    clf.fit(x_train, y_train.values.ravel()) # Fit to data
    supportVectors.append(clf.n_support_.sum()) # Record total number of support vectors

# Plot for c
supportVectors = np.asarray(supportVectors)
plt.scatter(C, supportVectors)
plt.xlabel('C Value')
plt.ylabel('Number of Support Vectors')
plt.title('Support Vectors vs Regularization Parameter')
#plt.show()

# D
Grid({'C' : [0.1,0.2,0.3,1,5,10,20,100,200,1000]}, 'linear', x_train, x_test, y_train, y_test)
Grid({'C' : [0.1,0.2,0.3,1,5,10,20,100,200,1000],
      'degree': [1,2,3,4,5],
      'coef0': [0.0001, 0.001, 0.002, 0.01, 0.02, 0.1, 0.2, 0.3, 1, 2, 5, 10]}, 'poly', x_train, x_test, y_train, y_test)
Grid({'C' : [0.1,0.2,0.3,1,5,10,20,100,200,1000],
      'gamma': [0.0001, 0.001, 0.002, 0.01, 0.02, 0.03, 0.1, 0.2, 1, 2, 3]}, 'rbf', x_train, x_test, y_train, y_test)
Grid({'C' : [0.1,0.2,0.3,1,5,10,20,100,200,1000],
      'coef0': [0.0001, 0.001, 0.002, 0.01, 0.02, 0.1, 0.2, 0.3, 1, 2, 5, 10],
      'gamma': [0.0001, 0.001, 0.002, 0.01, 0.02, 0.03, 0.1, 0.2, 1, 2, 3]}, 'sigmoid', x_train, x_test, y_train, y_test)

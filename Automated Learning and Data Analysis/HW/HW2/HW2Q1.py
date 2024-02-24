''' Code solution to HW2 Question 1. Using Principal Component Analysis to do stuff with train schedule data.
Date: 9/12/22      
'''
# Import packages I may need.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

# A) Load the data, report sizes of training and testing sets. How many class 0, class 1, and class 2 samples are
# in the training set and testing set, respectively?
ftrain = 'Data/pca_train.csv'
ftest = 'Data/pca_test.csv'
traindata = pd.read_csv(ftrain, header=0)
testdata = pd.read_csv(ftest, header=0)
trainDF = pd.DataFrame(traindata)
testDF = pd.DataFrame(testdata)


# Training set is 125 rows x 14 columns
# Testing set is 53 rows x 14 columns.
# print('The training dataset has a size of ' + str(trainDF.size) + ', and the testing dataset has a size of '
#       + str(testDF.size) +'. \n')

# Get class counts
# Train set: 37 Class 0, 51 Class 1, 37 Class 2
trcount1 = (trainDF.Class == 0).sum()
trcount2 = (trainDF.Class == 1).sum()
trcount3 = (trainDF.Class == 2).sum()

# Test set: 22 Class 0, 20 Class 1, 11 Class 2
testcount1 = (testDF.Class == 0).sum()
testcount2 = (testDF.Class == 1).sum()
testcount3 = (testDF.Class == 2).sum()

# print('The training set consists of the following number of class entries: \n'
#       'Class 0: ' + str(trcount1) + '\n'
#       'Class 1: ' + str(trcount2) + '\n'
#       'Class 2: ' + str(trcount3) + '\n')
# print('The testing set consists of the following numbers of class entries: \n'
#       'Class 0: ' + str(testcount1) + '\n'
#       'Class 1: ' + str(testcount2) + '\n'
#       'Class 2: ' + str(testcount3) + '\n')

# B) Run normalization on all input features in both datasets. (use min/max of each column in the training set to
# normalize the testing set, and do NOT normalize the output "Class".

def normalize(df):
    for column in df.columns:
        if column != 'Class':
            hi = df[column].max()
            lo = df[column].min()
            df[column] = (df[column] - lo) / (hi - lo)
    return df


norm_trainDF = normalize(trainDF)
norm_testDF = normalize(testDF)
traintarget = norm_trainDF['Class']
testtarget = pd.DataFrame(norm_testDF['Class'])
testtarget.rename(columns={'Class': 'Target Class'}, inplace=True)

# print(norm_trainDF)
# print(norm_testDF)

# B.i) Calculate the covariance matrix of the NEW training dataset. Specify 1) the dimension of the resulted covariance
# matrix and 2) please report the first 5 rows and 5 columns of the entire covariance matrix.
norm_trainDF.drop(columns='Class', inplace=True)
norm_testDF.drop(columns='Class', inplace=True)
traincov = norm_trainDF.cov()
# The covariance matrix is 13-dimensional.

sample = traincov.iloc[0:5, 0:5]
# print(sample.to_string())
# print('\n')

# B.ii) Calculate the eigenvalues and eigenvectors based on the entire covariance matrix. Report size of covariance
# matrix and its 5 largest eigenvalues.
eigs, vects = np.linalg.eig(traincov.astype(float))
largeeigs = sorted(eigs, reverse=True)[0:5]
# print('The normalized covariance matrix has size ' + str(traincov.size) + '.\n')
# print('Five largest eigenvalues, normalized: ' + str(largeeigs) + '\n')

# B.iii) Display the eigenvalues using a bar graph, and choose a reasonable number of eigenvectors. Justify answer.
# eigplot = plt.figure()
# num = ['1', '2', '3', '4', '5']
# plt.plot(num, largeeigs)
# plt.show()

# I would choose three eigenvectors, as the eigenvalues appear to nearly flatten out after the first three.
# In other words, the eigenvectors corresponding to the three largest eigenvalues contain the bulk of the information
# useful for our PCA analysis.

# B.iv) Combine PCA with a K-nearest neighbor (KNN) classifier. PCA will reduce dimensionality of original data into
# p principal components and KNN (K=5, use Euclidean distance) will  be employed to the p principal components for
# classification.
# B.iv.a) Report accuracy with p=5, generate .csv file with results
pca = PCA(n_components=5)
trainresult = pca.fit_transform(norm_trainDF)
trainresultDF = pd.DataFrame(trainresult)
testresult = pca.transform(norm_testDF)
testresultDF = pd.DataFrame(testresult, columns=['PC1', 'PC2', 'PC3', 'PC4', 'PC5'])

knn = KNN(n_neighbors=5, metric='euclidean')
knn.fit(trainresultDF, traintarget)
prediction = knn.predict(testresultDF)
# print(classification_report(testtarget, prediction))
prediction = pd.DataFrame(prediction, columns=['Predicted Class'])
results = pd.concat([testresultDF, testtarget, prediction], axis=1)
acc = accuracy_score(testtarget, prediction)
results.to_csv('Normalized PCA Results.csv', index=False)
# print(prediction)
# print(testtarget)

# B.iv.b) Plot results with varying number of principal components.
def plot_results(trainset, testset, traintarg, testtarg):
    plist = [1, 2, 3, 5, 10, 13]
    results = []
    for p in plist:
        entry = []
        entry.append(p)

        pca = PCA(n_components=p)
        trainresult = pca.fit_transform(trainset)
        trainresultDF = pd.DataFrame(trainresult)
        testresult = pca.transform(testset)
        testresultDF = pd.DataFrame(testresult)

        knn = KNN(n_neighbors=5, metric='euclidean')
        knn.fit(trainresultDF, traintarg)
        prediction = knn.predict(testresultDF)
        prediction = pd.DataFrame(prediction)
        acc = accuracy_score(testtarg, prediction)

        entry.append(acc)
        results.append(entry)
    results = pd.DataFrame(results, columns=['n Components', 'Accuracy'])
    return results

points = plot_results(norm_trainDF, norm_testDF, traintarget, testtarget)

# points.plot(x='n Components', y='Accuracy')
# plt.show()

# B.iv.c) What is the most reasonable number of principal components?
# I would say 5, as there does not seem to be any improvement in accuracy beyond that point. These results
# suggest that the first 5 principal components explain the vast majority of the variance observed in the dataset.

# C) Repeat all of the above, except standardize the data instead of normalize it.
# Standardize with sklearn tools
sc = StandardScaler()
sc.fit(trainDF)
std_train = sc.transform(trainDF)
std_trainDF = pd.DataFrame(std_train, columns=norm_trainDF.columns)

sc.fit(testDF)
std_test = sc.transform(testDF)
std_testDF = pd.DataFrame(std_test, columns=norm_testDF.columns)

# C.i) Calculate the covariance matrix of the NEW training dataset. Specify 1) the dimension of the resulted covariance
# matrix and 2) please report the first 5 rows and 5 columns of the entire covariance matrix.
traincov2 = std_trainDF.cov()
# The covariance matrix is 13-dimensional.

sample2 = traincov.iloc[0:5, 0:5]
# print(sample2.to_string())
# print('\n')

# C.ii) Calculate the eigenvalues and eigenvectors based on the entire covariance matrix. Report size of covariance
# matrix and its 5 largest eigenvalues.
eigs2, vects2 = np.linalg.eig(traincov2.astype(float))
largeeigs2 = sorted(eigs2, reverse=True)[0:5]
# print('The standardized covariance matrix has size ' + str(traincov2.size) + '.\n')
# print('Five largest eigenvalues, standardized: ' + str(largeeigs2) + '\n')

# C.iii) Display the eigenvalues using a bar graph, and choose a reasonable number of eigenvectors. Justify answer.
eigplot2 = plt.figure()
num2 = ['1', '2', '3', '4', '5']
plt.plot(num2, largeeigs2)
plt.show()

# I would choose at least five eigenvectors, as the eigenvalues do not appear to flatten out on the shown curve.
# This leads me to believe that the first 5 principal components do not fully explain the variance.

# C.iv) Combine PCA with a K-nearest neighbor (KNN) classifier. PCA will reduce dimensionality of original data into
# p principal components and KNN (K=5, use Euclidean distance) will  be employed to the p principal components for
# classification.
# C.iv.a
pca = PCA(n_components=5)
trainresult = pca.fit_transform(std_trainDF)
trainresultDF = pd.DataFrame(trainresult)
testresult = pca.transform(std_testDF)
testresultDF = pd.DataFrame(testresult, columns=['PC1', 'PC2', 'PC3', 'PC4', 'PC5'])

knn = KNN(n_neighbors=5, metric='euclidean')
knn.fit(trainresultDF, traintarget)
prediction = knn.predict(testresultDF)
# print(classification_report(testtarget, prediction))
prediction = pd.DataFrame(prediction, columns=['Predicted Class'])
results = pd.concat([testresultDF, testtarget, prediction], axis=1)
acc2 = accuracy_score(testtarget, prediction)
# print('The accuracy using the standardized data with 5 principal components and 5 nearest neighbors is ' + str(acc2) +
#       '.')
# results.to_csv('Standardized PCA Results.csv', index=False)

# C.iv.b) Plot results with varying number of principal components.
points2 = plot_results(std_trainDF, std_testDF, traintarget, testtarget)
# print(points2)
points2.plot(x='n Components', y='Accuracy')
plt.show()


# C.iv.c) This time it appears that the most reasonable choice is 2 principal components. It does not
# make sense to me that we got the results we did here...

# D) Of the two results between normalized and standardized data, I would prefer to use the standardized data
# as it is able to give a comparable best accuracy (around 98%) to the normalized data using 2 principal components
# instead of 5 principal components as with the normalized data.
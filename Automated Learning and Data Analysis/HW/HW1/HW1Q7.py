import pandas as pd
import matplotlib.pyplot as plt
import math

# A) Import and clean data. THen produce a scatter plot between RH and Ws. Label the axes. Title plot 'relative humidity
# and wind speed'. What general interpretation can you make from this plot?
# Import and clean up the dataset
data = 'Algerian_forest_fires_dataset_UPDATE.csv'
df = pd.read_csv(data, header=1)
df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
df.drop(index=123, inplace=True)

# Since we are only concerned with RH and Ws, we'll grab those columns and make a new DF with the relevant data
reldat = df[[' RH', ' Ws']].copy()
reldat.rename(columns={' RH': 'RH', ' Ws': 'Ws'}, inplace=True)
reldat['RH'] = reldat['RH'].astype(float)
reldat['Ws'] = reldat['Ws'].astype(float)
plt.figure()
reldat.plot(kind='scatter', x='RH', y='Ws', title='relative humidity and wind speed')
plt.show()

# General interpretation -- wind speed does not appear to correlate strongly with relative humidity

# B) Define point P = (mean(RH), mean(Ws))
P = (reldat['RH'].mean(), reldat['Ws'].mean())

# C) Compute distance between P and each data point using: 1) Euclidean distance, 2) Manhattan block metric,
# 3) Minkowski metric (for power=7), 4) Chebyshev distance, and 5) Cosine distance. List the 6 closest points
# for each distance.

# Start by getting the list of points
pointlist = []
for index, rows in reldat.iterrows():
    entry = [rows.RH, rows.Ws]
    pointlist.append(entry)

# 1) Euclidean distance function. Takes the point P and the pointlist and returns a list of distances that can be appended to
# the original dataframe.
def euclidean(point, points):
    euc = []
    x1 = point[0]
    y1 = point[1]
    for item in points:
        x2 = item[0]
        y2 = item[1]
        dist = round(math.sqrt(((x2-x1)**2) + ((y2-y1)**2)), 2)
        euc.append(dist)
    return euc

ED = euclidean(P, pointlist)
reldat['Euclidean Distance'] = ED

# 2) Manhattan distance.

def manhattan(point, points):
    man = []
    x1 = point[0]
    y1 = point[1]
    for item in points:
        x2 = item[0]
        y2 = item[1]
        dist = round(abs(x1-x2) + abs(y1-y2), 2)
        man.append(dist)
    return man

man = manhattan(P, pointlist)
reldat['Manhattan Distance'] = man

# 3) Minkowski metric for power=7
def minkowski(point, points):
    mink = []
    x1 = point[0]
    y1 = point[1]
    for item in points:
        x2 = item[0]
        y2 = item[1]
        dist = round((((abs(x1-x2)**7) + (abs(y1-y2)**7)) ** (1/7)), 2)
        mink.append(dist)
    return mink

mink = minkowski(P, pointlist)
reldat['Minkowski Distance'] = mink

# 4) Chebyshev distance
def chebyshev(point, points):
    cheb = []
    x1 = point[0]
    y1 = point[1]
    for item in points:
        x2 = item[0]
        y2 = item[1]
        dist = round(max(abs(x2-x1), abs(y2-y1)), 2)
        cheb.append(dist)
    return cheb

cheb = chebyshev(P, pointlist)
reldat['Chebyshev Distance'] = cheb

# 5) Cosine distance
def cosine(point, points):
    cos = []
    x1 = point[0]
    y1 = point[1]
    for item in points:
        x2 = item[0]
        y2 = item[1]
        num = (x1*y1) + (x2*y2)
        denomL = math.sqrt(x1**2 + x2**2)
        denomR = math.sqrt(y1**2 + y2**2)
        denom = denomL*denomR
        cossim = num / denom
        dist = round(1 - cossim, 5)
        cos.append(dist)
    return cos

cos = cosine(P, pointlist)
reldat['Cosine Distance'] = cos

# List the closest 6 points for each distance
# Euclidean
smallesteuc = reldat.nsmallest(6, ['Euclidean Distance'])
smallesteuc = smallesteuc.get(['RH', 'Ws', 'Euclidean Distance'])
print('Euclidean')
print(smallesteuc.to_string())
print('\n')

# Manhattan
smallestman = reldat.nsmallest(6, ['Manhattan Distance'])
smallestman = smallestman.get(['RH', 'Ws', 'Manhattan Distance'])
print('Manhattan')
print(smallestman.to_string())
print('\n')

# Minkowski
smallestmink = reldat.nsmallest(6, ['Minkowski Distance'])
smallestmink = smallestmink.get(['RH', 'Ws', 'Minkowski Distance'])
print('Minkowski')
print(smallestmink.to_string())
print('\n')

# Chebyshev
smallestcheb = reldat.nsmallest(6, ['Chebyshev Distance'])
smallestcheb = smallestcheb.get(['RH', 'Ws', 'Chebyshev Distance'])
print('Chebyshev')
print(smallestcheb.to_string())
print('\n')

# Cosine
smallestcos = reldat.nsmallest(6, ['Cosine Distance'])
smallestcos = smallestcos.get(['RH', 'Ws', 'Cosine Distance'])
print('Cosine')
print(smallestcos.to_string())
print('\n')

# D) For each distance measure identify the 20 points from the dataset that are closest to the point P.
# i) Create a plot for each distance measure. Place P and mark the 20 closest points. Use different colors
# or shapes to mark them. Make sure the points can be uniquely identified.

eucpoints = reldat.nsmallest(20, ['Euclidean Distance'])
manpoints = reldat.nsmallest(20, ['Manhattan Distance'])
minkpoints = reldat.nsmallest(20, ['Minkowski Distance'])
chebpoints = reldat.nsmallest(20, ['Chebyshev Distance'])
cospoints = reldat.nsmallest(20, ['Cosine Distance'])

# Euclidean plot
eucind = eucpoints.index
todrop = []
for x in eucind:
    todrop.append(x)
eucremain = reldat.drop(todrop)


plt.figure()
Pdf = pd.DataFrame([P], columns=['RH', 'Ws'])
eucplot = eucremain.plot(kind='scatter', x='RH', y='Ws', color='blue', title='Euclidean', s=5)
Pdf.plot(ax=eucplot, kind='scatter', x='RH', y='Ws', color='red')
eucpoints.plot(ax=eucplot, kind='scatter', x='RH', y='Ws', color='green', marker='*', s=5)
plt.show()

# Manhattan plot
manind = manpoints.index
todrop = []
for x in manind:
    todrop.append(x)
manremain = reldat.drop(todrop)

plt.figure()
manplot = manremain.plot(kind='scatter', x='RH', y='Ws', color='blue', title='Manhattan', s=5)
Pdf.plot(ax=manplot, kind='scatter', x='RH', y='Ws', color='red')
manpoints.plot(ax=manplot, kind='scatter', x='RH', y='Ws', color='green', marker='*', s=5)
plt.show()

# Minkowski
minkind = minkpoints.index
todrop = []
for x in minkind:
    todrop.append(x)
minkremain = reldat.drop(todrop)

plt.figure()
minkplot = minkremain.plot(kind='scatter', x='RH', y='Ws', color='blue', title='Minkowski', s=5)
Pdf.plot(ax=minkplot, kind='scatter', x='RH', y='Ws', color='red')
minkpoints.plot(ax=minkplot, kind='scatter', x='RH', y='Ws', color='green', marker='*', s=5)
plt.show()

# Chebyshev
chebind = chebpoints.index
todrop = []
for x in chebind:
    todrop.append(x)
chebremain = reldat.drop(todrop)

plt.figure()
chebplot = chebremain.plot(kind='scatter', x='RH', y='Ws', color='blue', title='Chebyshev', s=5)
Pdf.plot(ax=chebplot, kind='scatter', x='RH', y='Ws', color='red')
chebpoints.plot(ax=chebplot, kind='scatter', x='RH', y='Ws', color='green', marker='*', s=5)
plt.show()

# Cosine
cosind = cospoints.index
todrop = []
for x in cosind:
    todrop.append(x)
cosremain = reldat.drop(todrop)

plt.figure()
cosplot = cosremain.plot(kind='scatter', x='RH', y='Ws', color='blue', title='Cosine', s=5)
Pdf.plot(ax=cosplot, kind='scatter', x='RH', y='Ws', color='red')
cospoints.plot(ax=cosplot, kind='scatter', x='RH', y='Ws', color='green', marker='*', s=5)
plt.show()

# ii) Explanation in .pdf submission.
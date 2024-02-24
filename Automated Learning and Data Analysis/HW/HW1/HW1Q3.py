import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sbn
from scipy import stats


data = 'seeds_dataset.csv'

SeedDF = pd.read_csv(data)

# A) Compute mean, median, stdev, range, (25th, 50th, 75th) percentiles for: area, perimeter, length of kernel, width
# of kernel

# Area report
area = SeedDF['area'].describe()
area.loc['range'] = area.loc['max'] - area.loc['min']
area.loc['median'] = SeedDF['area'].median()
area.drop(['count', 'min', 'max'], inplace=True)
print('Area Report')
print(area)
print('\n')

# Perimeter report
perim = SeedDF['perimeter'].describe()
perim.loc['range'] = perim.loc['max'] - perim.loc['min']
perim.loc['median'] = SeedDF['perimeter'].median()
perim.drop(['count', 'min', 'max'], inplace=True)
print('Perimeter Report')
print(perim)
print('\n')

# Length of kernel report
kl = SeedDF['length of kernel'].describe()
kl.loc['range'] = kl.loc['max'] - kl.loc['min']
kl.loc['median'] = SeedDF['length of kernel'].median()
kl.drop(['count', 'min', 'max'], inplace=True)
print('Kernel Length Report')
print(kl)
print('\n')

# Width of kernel
kw = SeedDF['width of kernel'].describe()
kw.loc['range'] = kw.loc['max'] - kw.loc['min']
kw.loc['median'] = SeedDF['width of kernel'].median()
kw.drop(['count', 'min', 'max'], inplace=True)
print('Kernel Width Report')
print(kw)
print('\n')

# B) Make a box-and-whisker plot for the attributes length of kernel and width of kernel where they are grouped by the
# class label. Include a title for each plot of what feature is being described.
plt.figure()
boxplot = SeedDF.boxplot(column=['length of kernel', 'width of kernel'], by='class')
plt.show()


# C) Make a histogram plot w/ 16 bins for the two features asymmetry coefficient and compactness, respectively
plt.figure()
hist = SeedDF.hist(column=['asymmetry coefficient', 'compactness'], bins=16)
plt.show()

# D) Make a scatter matrix with area, compactness, length of kernel, width of kernel. Use class attribute to change the color of
# data points. For diagonal of scatter matrix, plot kernel density estimation
plt.figure()
scatdf = pd.melt(SeedDF, id_vars=['area', 'compactness', 'length of kernel', 'width of kernel'], value_vars=['class'])
sbn.pairplot(scatdf, hue='value', diag_kind='kde')
plt.show()

# E) Produce 3D scatter plot using length of kernel, width of kernel, and area as dimensions, and color data points
# according to class attribute
sbn.set()
scatplot = plt.figure(figsize=(10,10))
ax = plt.axes(projection='3d')

dfmelt1 = scatdf.loc[scatdf['value']==1.0]
dfmelt2 = scatdf.loc[scatdf['value']==2.0]
dfmelt3 = scatdf.loc[scatdf['value']==3.0]

ax.scatter3D(dfmelt1['length of kernel'], dfmelt1['width of kernel'], dfmelt1['area'], color='red', label='Class 1')
ax.scatter3D(dfmelt2['length of kernel'], dfmelt2['width of kernel'], dfmelt2['area'], color='green', label='Class 2')
ax.scatter3D(dfmelt3['length of kernel'], dfmelt3['width of kernel'], dfmelt3['area'], color='blue', label='Class 3')

ax.set_xlabel('Length of Kernel')
ax.set_ylabel('Width of Kernel')
ax.set_zlabel('Area')

ax.legend()

plt.show()

# F) Create a quantile quantile plot for length of kernel groove and compactness. Give a brief analysis for the two
# plots.

groove = SeedDF['length of kernel groove']
comp = SeedDF['compactness']
plt.figure()
qq1 = stats.probplot(groove, plot=plt)
plt.title('length of kernel groove q-q plot')
plt.show()
plt.figure()
qq2 = stats.probplot(comp, plot=plt)
plt.title('compactness q-q plot')
plt.show()
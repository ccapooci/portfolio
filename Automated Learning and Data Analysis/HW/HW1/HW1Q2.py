import numpy as np
import math as m
np.random.seed(2022)

# Question 2
# a
a = np.identity(5)
print('a =')
print(a)

# b
a[:, 4] = 5
print('a =')
print(a)

# c
sum = 0
for x in np.nditer(a):
    sum += x
print('sum =')
print(sum)

# d
a = a.T
print('a =')
print(a)

# e
print('sums =')
sum = 0
for x in a[4, :]:
    sum += x
print(sum)
sum = 0
for x in np.diagonal(a):
    sum += x
print(sum)
sum = 0
for x in a[:, 0]:
    sum += x
print(sum)
    
# f
b = np.random.standard_normal((5, 5))
print('b =')
print(b)

# g
c = np.empty((2, 5))
c[0, :] = np.subtract(b[0, :], a[0, :])
c[1, :] = np.add(a[4, :], b[4, :])
print('c =')
print(c)

# h
d = np.multiply(np.arange(1,6,1), c)
print('d =')
print(d)

# i
x = np.array([1,1,1,2]).T
y = np.array([0,3,6,9]).T
z = np.array([4,3,2,1]).T
covmatrix = np.cov([x,y,z])
ccxy = np.corrcoef(x,y)

print("Covariance Matrix")
print(covmatrix)
print("Correlation Coefficients")
print(ccxy)

# j
x = np.array([23,19,21,22,21,23,23,20]).T
xm = np.mean(x)
xsm = np.mean(x**2)

print("xsm = ")
print(xsm)

xpstd = np.std(x)
xbar = (xm**2)+(xpstd**2)

print("xbar = ")
print(xbar)

xsstd = np.std(x, ddof=1)
xbar = (xm**2)+(xsstd**2)

print("xbar = ")
print(xbar)







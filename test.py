#min&max



import statistics
from scipy import stats
import matplotlib.pyplot as plt

# min & max
min([1,2,3,4])
max([1,2,3,4])

# varaince, mean, median, mode
print(statistics.variance([1, 3, 5, 7, 9, 11]))
print(statistics.mean([1, 3, 5, 7, 9, 11]))
print(statistics.median([1, 3, 5, 7, 9, 11, 13]))
print(statistics.mode([1, 3, 3, 3, 5, 7, 7, 9, 11]))



x = [5,7,8,7,2,17,2,9,4,11,12,9,6]
y = [99,86,87,88,111,86,103,87,94,78,77,85,86]

# plotXY
plt.scatter(x,y)
plt.show()



# Regression
slope, intercept, _, _, _ = stats.linregress(x, y)

def myfunc(x):
  return slope * x + intercept

mymodel = list(map(myfunc, x))

plt.scatter(x, y)
plt.plot(x, mymodel)
plt.show() 
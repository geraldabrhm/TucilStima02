import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from myConvexHull import *


from sklearn import datasets
data = datasets.load_wine()

df = pd.DataFrame(data.data, columns=data.feature_names)
df['Target'] = pd.DataFrame(data.target)

plt.figure(figsize = (10, 6))
colors = ['b','r','g']
plt.title('flavanoids vs nonflavanoid_phenols')
plt.xlabel(data.feature_names[6])
plt.ylabel(data.feature_names[7])

for i in range(len(data.target_names)):
    bucket = df[df['Target'] == i]
    bucket = bucket.iloc[:,[0,1]].values
    lp, rp = leftestRightest(bucket)
    hull = convexHull(bucket, lp, rp)
    plt.scatter(bucket[:, 0], bucket[:, 1], label=data.target_names[i])
    for simplex in hull:
        plt.plot(simplex[0], simplex[1], colors[i])
plt.legend()
plt.show()
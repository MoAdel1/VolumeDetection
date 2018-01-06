# code imports
import numpy as np
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
# define train data wth all orders
x = np.array([1,2,3,4]).reshape(-1, 1)  # shape(#rows,1)
poly = PolynomialFeatures(degree=3)
x_new = poly.fit_transform(x)
# get target 
target = np.array([1,2,3,4]).reshape(-1, 1)
target = target+0
# train model
regression_model = linear_model.LinearRegression(fit_intercept=False,copy_X=True,normalize=False)
regression_model.fit(x_new,target)
# get fitted curve
fitted = regression_model.predict(x_new)
# plot the fit
plt.scatter(x, target,  color='black')
plt.plot(x, fitted, color='blue', linewidth=2)
plt.xticks(())
plt.yticks(())
plt.show()



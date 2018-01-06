import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as axes3d


def f(x,b):
    return(-x**2 + b)
f = np.vectorize(f,otypes=[np.float])


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')

u = np.linspace(-1, 1, 30) # x range and number of points taken
v = np.linspace(0, 2*np.pi, 30) # orientation range
U, V = np.meshgrid(u, v)

X = U   # original x axis
Y = f(U,1)*np.cos(V)  # y axis projection
Z = f(U,1)*np.sin(V)  # z axis projection



ax.plot_surface(X, Y, Z, color='red')
ax.set_yticklabels([])
ax.set_xticklabels([])
ax.set_zticklabels([])



plt.show()

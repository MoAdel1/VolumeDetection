import matplotlib.pyplot as plt

fig = plt.figure()
fig.suptitle("Main title of every thing else",fontsize=16)

ax1 = fig.add_subplot(1,2,1)
ax1.plot([1,2,3,4,5], [10,5,10,5,10], 'r-')
ax1.set_yticklabels([])
ax1.set_xticklabels([])
ax1.set_title("first")

ax2 = fig.add_subplot(1,2,2)
ax2.plot([1,2,3,4], [1,4,9,16], 'k-')
ax2.set_yticklabels([])
ax2.set_xticklabels([])
ax2.set_title("second")






plt.show()

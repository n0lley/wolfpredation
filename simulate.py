from map import Map
from tile import Tile
import constants as c
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import os
import pickle

np.random.seed(111)

map = Map()
mplot = map.plotMap()

fig = plt.figure()
ax = fig.add_subplot(111)

dpop = []
wpop = []
"""
cmap = colors.ListedColormap(["green","black","brown"])
ax.imshow(mplot, interpolation='nearest', cmap=cmap)
plt.axis('off')
plt.savefig("./data/gen.png")
plt.close()

for i in range(100):
    print(i)
    w, d = map.update(i)
    dpop.append(d)
    wpop.append(w)
    if d <= 1 or w <= 1:
        break
    mplot = map.plotMap()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(mplot, interpolation='nearest', cmap=cmap)
    plt.axis('off')
    plt.savefig("./data/gen%d.png"%i)
    plt.close()
    f = open("./data/plot.p", 'wb')
    pickle.dump([dpop, wpop], f)
    f.close()
"""
f = open("./data/plot.p", 'rb')
pops = pickle.load(f)
f.close()
dpop = pops[0]
wpop = pops[1]
x = np.linspace(0,99,100)
plt.plot(x, dpop, label="elk")
plt.plot(x, wpop, label="wolves")
plt.xlabel("Time Steps")
plt.ylabel("Number of Individuals")
plt.title("Change in Yellowstone Predator and Prey Populations Over Time")
plt.legend()
plt.show()

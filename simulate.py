from map import Map
from tile import Tile
import constants as c
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import os

map = Map()
mplot = map.plotMap()

fig = plt.figure()
ax = fig.add_subplot(111)

dpop = []
wpop = []

cmap = colors.ListedColormap(["green","black","brown"])
ax.imshow(mplot, interpolation='nearest', cmap=cmap)
plt.savefig("./data/gen.png")
plt.close()

for i in range(1000):
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
    plt.savefig("./data/gen%d.png"%i)
    plt.close()

x = np.linspace(0,i,i+1)
plt.plot(x, dpop, label="elk")
plt.plot(x, wpop, label="wolves")
plt.legend()
plt.show()

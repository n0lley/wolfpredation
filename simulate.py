from map import Map
#from wolf import Wolf
from deer import Deer
from tile import Tile
import constants as c
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import os

map = Map()
mplot = map.plotMap()

fig = plt.figure()
ax = fig.add_subplot(111)

cmap = colors.ListedColormap(["green","black","brown"])
ax.imshow(mplot, interpolation='nearest', cmap=cmap)
plt.savefig("./data/gen.png")
plt.close()

for i in range(1000):
    print(i)
    w, d = map.update(i)
    if d == 0 or w==0:
        break
    mplot = map.plotMap()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(mplot, interpolation='nearest', cmap=cmap)
    plt.savefig("./data/gen%d.png"%i)
    plt.close()

from map import Map
#from wolf import Wolf
from deer import Deer
from tile import Tile
import constants as c
import matplotlib.pyplot as plt
import matplotlib.colors as colors

map = Map()
mplot = map.plotMap()

fig = plt.figure()
ax = fig.add_subplot(111)

cmap = colors.ListedColormap(["green","black","brown"])
ax.imshow(mplot, interpolation='nearest', cmap=cmap)
plt.show()

for i in range(10):
    map.update()

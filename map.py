import constants as c
import numpy as np
from tile import Tile
from deer import Deer
from wolf import Wolf

class Map:

    def __init__(self):

        totalarea = c.MAPSIZE[0] * c.MAPSIZE[1]
        self.map = []
        self.wolves = []
        self.deer = []
        
        for x in range(c.MAPSIZE[0]):
            self.map.append([])
            for y in range(c.MAPSIZE[1]):
                self.map[x].append(Tile([x,y]))
                """
                if np.random.random() < (c.INITDEER/totalarea):
                    self.map[x][y].id = "deer"
                    self.map[x][y].addAnimal(Deer([x,y]))
                """
        for x in range(int(c.MAPSIZE[0]/2) - 5, int(c.MAPSIZE[0]/2) + 5):
            for y in range(int(c.MAPSIZE[1]/2) - 5, int(c.MAPSIZE[1]/2) + 5):
                if np.random.random() < c.INITWOLVES/100:
                    self.map[x][y].id = "wolf"
                    self.map[x][y].addAnimal(Wolf([x,y]))
                    self.wolves.append([x,y])
                    
    def update(self):
        for w in self.wolves:
            xloc = w[0]
            yloc = w[1]
            tile = self.map[xloc][yloc]
            wolf = tile.animal
            neighborhood = []
            xlow = xloc - c.WOLFSENSERADIUS
            if xlow < 0:
                xlow = 0
            xhi = xloc + c.WOLFSENSERADIUS
            if xhi > c.MAPSIZE[0]-1:
                xhi = c.MAPSIZE[0]-1
            ylow = yloc - c.WOLFSENSERADIUS
            if ylow < 0:
                ylow = 0
            yhi = yloc + c.WOLFSENSERADIUS
            if yhi > c.MAPSIZE[1]-1:
                yhi = c.MAPSIZE[1]-1
            neighborhood = self.map[xlow:xhi+1]
            for col in neighborhood:
                col = col[ylow:yhi+1]
            wolf.move(neighborhood)

    def plotMap(self):
        
        mapplot = []
        for x in range(len(self.map)):
            mapplot.append([])
            for y in range(len(self.map[0])):
                if self.map[x][y].id == "wolf":
                    mapplot[x].append(1)
                elif self.map[x][y].id == "deer":
                    mapplot[x].append(2)
                else:
                    mapplot[x].append(0)

        return mapplot

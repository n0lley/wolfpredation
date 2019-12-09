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
                
                if np.random.random() < (c.INITDEER/totalarea):
                    self.map[x][y].id = "deer"
                    self.map[x][y].addAnimal(Deer([x,y]))
                    self.deer.append((x,y))
        
        for x in range(int(c.MAPSIZE[0]/2) - 5, int(c.MAPSIZE[0]/2) + 5):
            for y in range(int(c.MAPSIZE[1]/2) - 5, int(c.MAPSIZE[1]/2) + 5):
                if np.random.random() < c.INITWOLVES/100 and self.map[x][y].id == "empty":
                    self.map[x][y].id = "wolf"
                    self.map[x][y].addAnimal(Wolf([x,y]))
                    self.wolves.append((x,y))
                    
    def update(self, time):
    
        #TODO: die
    
        #move wolves
        tmpwolves = {}
        for w in self.wolves:
            #move the wolf
            tile = self.map[w[0]][w[1]]
            wolf = tile.animal
            
            neighborhood = []
            xlow = w[0] - c.WOLFSENSERADIUS
            if xlow < 0:
                xlow = 0
            xhi = w[0] + c.WOLFSENSERADIUS
            if xhi > c.MAPSIZE[0]-1:
                xhi = c.MAPSIZE[0]-1
            ylow = w[1] - c.WOLFSENSERADIUS
            if ylow < 0:
                ylow = 0
            yhi = w[1] + c.WOLFSENSERADIUS
            if yhi > c.MAPSIZE[1]-1:
                yhi = c.MAPSIZE[1]-1
            neighborhood = self.map[xlow:xhi+1]
            for col in neighborhood:
                col = col[ylow:yhi+1]
                
            wolf.move(neighborhood)
            
            x = wolf.coords[0]
            y = wolf.coords[1]
                
            while (x, y) in list(tmpwolves.keys()) or x>=c.MAPSIZE[0] or y>=c.MAPSIZE[1] or x<0 or y<0:
                d = np.random.choice([-1,0,1], size=2)
                x += d[0]
                y += d[1]
            
            wolf.coords[0] = x
            wolf.coords[1] = y
            tmpwolves[(wolf.coords[0],wolf.coords[1])] = wolf
        
        #move deer
        tmpdeer = {}
        for d in self.deer:
            #move the deer
            xloc = d[0]
            yloc = d[1]
            tile = self.map[xloc][yloc]
            deer = tile.animal
            neighborhood = []
            xlow = xloc - c.DEERSENSERADIUS
            if xlow < 0:
                xlow = 0
            xhi = xloc + c.DEERSENSERADIUS
            if xhi > c.MAPSIZE[0]-1:
                xhi = c.MAPSIZE[0]-1
            ylow = yloc - c.DEERSENSERADIUS
            if ylow < 0:
                ylow = 0
            yhi = yloc + c.DEERSENSERADIUS
            if yhi > c.MAPSIZE[1]-1:
                yhi = c.MAPSIZE[1]-1
            neighborhood = self.map[xlow:xhi+1]
            for col in neighborhood:
                col = col[ylow:yhi+1]
                
            deer.move(neighborhood)
            
            x = deer.coords[0]
            y = deer.coords[1]
            while (x, y) in list(tmpdeer.keys()) or x>=c.MAPSIZE[0] or y>=c.MAPSIZE[1] or x<0 or y<0 or (x,y) in list(tmpwolves.keys()):
                d = np.random.choice([-1,0,1], size=2)
                x += d[0]
                y += d[1]
           
            deer.coords[0] = x
            deer.coords[1] = y
            tmpdeer[(deer.coords[0],deer.coords[1])] = deer
        
        for d in self.deer:
            self.map[d[0]][d[1]].clear()
        for w in self.wolves:
            self.map[w[0]][w[1]].clear()
            
        self.wolves = list(tmpwolves.keys())
        self.deer = list(tmpdeer.keys())
         
        #place wolves
        for w in self.wolves:
        
            x = w[0]
            y = w[1]
                
            self.map[x][y].id = "wolf"
            tmpwolves[w].coords = [x,y]
            self.map[x][y].addAnimal(tmpwolves[w])
        
        #place deer
        for d in self.deer:
        
            x = d[0]
            y = d[1]
            
            if x < 0 or x >= c.MAPSIZE[0] or y < 0 or y >= c.MAPSIZE[1]:
                print(d)
                
            self.map[x][y].id = "deer"
            tmpdeer[d].coords = [x,y]
            self.map[x][y].addAnimal(tmpdeer[d])
        #self.scan()
        
        #wolves eat deer
        for w in self.wolves:
            #get neighborhood
            tile = self.map[w[0]][w[1]]
            wolf = tile.animal
            
            neighborhood = []
            xlow = w[0] - 1
            if xlow < 0:
                xlow = 0
            xhi = w[0] + 1
            if xhi > c.MAPSIZE[0]-1:
                xhi = c.MAPSIZE[0]-1
            ylow = w[1] - 1
            if ylow < 0:
                ylow = 0
            yhi = w[1] + 1
            if yhi > c.MAPSIZE[1]-1:
                yhi = c.MAPSIZE[1]-1
            neighborhood = self.map[xlow:xhi+1]
            for col in neighborhood:
                col = col[ylow:yhi+1]
                
            prey = wolf.eat(neighborhood)
            if prey is not None:
                tmpx = prey[0]
                tmpy = prey[1]
                self.deer.remove((tmpx,tmpy))
                self.map[tmpx][tmpy].clear()
            
            print("Wolves:",len(self.wolves),"Deer:",len(self.deer))
        """
        #if on the xth timestep, reproduce
        if time%c.REPRODUCTIONRATE == 0:
            for w in self.wolves:
                wolf = self.map[w[0]][w[1]].animal
                wolf.reproduce()
            
            for d in self.deer:
                deer = self.map[d[0]][d[1]].animal
                deer.reproduce()
"""
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

    def scan(self):
        print("---------------------")
        for d in self.deer:
            if d[0] in range(len(self.map)) and d[1] in range(len(self.map[0])):
                print(d, end=', ')
                print(self.map[d[0]][d[1]].id)
            else:
                print(d)
        
        print("+++++++++++++++++++++")

        for w in self.wolves:
            if w[0] in range(len(self.map)) and w[1] in range(len(self.map[0])):
                print(w, end=', ')
                print(self.map[w[0]][w[1]].id)
            else:
                print(w)
        print("---------------------")

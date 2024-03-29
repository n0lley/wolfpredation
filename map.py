import constants as c
import numpy as np
from tile import Tile
from deer import Deer
from wolf import Wolf
from copy import deepcopy

class Map:

    def __init__(self):

        totalarea = c.MAPSIZE[0] * c.MAPSIZE[1]
        self.map = []
        self.wolves = {}
        self.deer = {}
        
        for x in range(c.MAPSIZE[0]):
            self.map.append([])
            for y in range(c.MAPSIZE[1]):
                self.map[x].append(Tile([x,y]))
                
                if np.random.random() < (c.INITDEER/totalarea):
                    self.map[x][y].id = "deer"
                    self.map[x][y].addAnimal(Deer())
                    self.deer[(x,y)] = self.map[x][y].animal
        
        while len(self.wolves) < c.INITWOLVES:
            x = np.random.randint(c.MAPSIZE[0]/2-5, c.MAPSIZE[0]/2+5)
            y = np.random.randint(c.MAPSIZE[1]/2-5, c.MAPSIZE[1]/2+5)
            if self.map[x][y].id == "empty":
                self.map[x][y].id = "wolf"
                self.map[x][y].addAnimal(Wolf())
                self.wolves[(x,y)] = self.map[x][y].animal
                    
    def update(self, time):
    
        wtodel = []
        for w in self.wolves:
            wolf = self.wolves[w]
            if wolf.energy <= 0:
                wtodel.append(w)
        for w in wtodel:
            del self.wolves[w]
            self.map[w[0]][w[1]].clear()
                
        dtodel = []
        for d in self.deer:
            deer = self.deer[d]
            n = self.getNeighborhood(d, 1)
            surrounded = True
            for col in n:
                for tile in col:
                    if tile.id == "empty":
                        surrounded = False
            if deer.energy <= 0:
                dtodel.append(d)
            if surrounded:
                dtodel.append(d)
                
        for d in dtodel:
            del self.deer[d]
            self.map[d[0]][d[1]].clear()
    
        #move wolves
        tmpwolves = {}
        for w in self.wolves:
            #move the wolf
            wolf = self.wolves[w]
        
            wolf.energy -= c.WOLFDECAY
            
            x = w[0]
            y = w[1]
        
            neighborhood = self.getNeighborhood((x,y), c.WOLFSENSERADIUS)
                
            x,y = wolf.move(w, neighborhood)
                
            #if the space we're trying to occupy is already taken
            if (x, y) in list(tmpwolves.keys()) or self.map[x][y].id != "empty" or x<0 or y<0 or x>=c.MAPSIZE[0] or y>=c.MAPSIZE[1]:
                x,y = w[0],w[1]
            
            tmpwolves[(x,y)] = wolf
        
        #move deer
        tmpdeer = {}
        for d in self.deer:
            
            x = d[0]
            y = d[1]
            deer.energy += 2
            #move the deer
            
            deer = self.deer[d]
            
            neighborhood = self.getNeighborhood(d, c.DEERSENSERADIUS)
                
            x,y = deer.move(d, neighborhood)
            
            #if the space we're trying to occupy is taken
            disp = 1
            if (x, y) in list(tmpwolves.keys()) or self.map[x][y].id != "empty" or (x,y) in list(tmpdeer.keys()) or x<0 or y<0 or x>=c.MAPSIZE[0] or y>=c.MAPSIZE[1]:
                x,y = d[0],d[1]
                    
            tmpdeer[(x,y)] = deer
            
        for w in self.wolves:
            x,y = w[0],w[1]
            self.map[x][y].clear()
        for d in self.deer:
            x,y = d[0],d[1]
            self.map[x][y].clear()
            
        self.wolves = tmpwolves
        self.deer = tmpdeer
         
        #place wolves
        for w in self.wolves:
        
            x = w[0]
            y = w[1]
                
            self.map[x][y].id = "wolf"
            self.map[x][y].addAnimal(tmpwolves[w])
        
        #place deer
        for d in self.deer:
        
            x = d[0]
            y = d[1]
                
            self.map[x][y].id = "deer"
            self.map[x][y].addAnimal(tmpdeer[d])
        
        #wolves eat deer
        for w in self.wolves:
            #get neighborhood
            tile = self.map[w[0]][w[1]]
            wolf = tile.animal
            
            neighborhood = self.getNeighborhood(w, 2)
                
            prey = wolf.eat(neighborhood)
            if prey is not None:
                tmpx = prey[0]
                tmpy = prey[1]
                del self.deer[(tmpx, tmpy)]
                self.map[tmpx][tmpy].clear()
                
                wlist = []
                n = self.getNeighborhood(w, 10)
                for col in n:
                    for tile in col:
                        if tile.id == "wolf":
                            wlist.append(tile.coords)
                
                for w in wlist:
                    x = w[0]
                    y = w[1]
                    self.wolves[(x,y)].energy += int(150/len(wlist))
            
        #print(list(self.deer.keys()))
        print("Wolves:",len(self.wolves),"Deer:",len(self.deer))
        
        #if on the xth timestep, reproduce
        #if time%c.REPRODUCTIONRATE == 0:
        if True:
            newwolves = {}
            for w in self.wolves:
                wolf = self.wolves[w]
                if wolf.energy >=80:
                    neighborhood = self.getNeighborhood(w,5)
                    newwolf, coords = wolf.reproduce(w, neighborhood)
                    if newwolf != None:
                        newwolves[coords] = newwolf
                        
            for w in newwolves:
                self.wolves[w] = deepcopy(newwolves[w])
                self.map[w[0]][w[1]].id = "wolf"
                self.map[w[0]][w[1]].addAnimal(self.wolves[w])
                
            newdeers = {}
            for d in self.deer:
                deer = self.deer[d]
                if np.random.random() < c.DEERBIRTHCHANCE and deer.energy > 80:
                    neighborhood = self.getNeighborhood(d,5)
                    newdeer, coords = deer.reproduce(d, neighborhood)
                    if newdeer != None:
                        newdeers[coords] = newdeer
            for d in newdeers:
                self.deer[d] = deepcopy(newdeers[d])
                self.map[d[0]][d[1]].id = "deer"
                self.map[d[0]][d[1]].addAnimal(self.deer[d])

        return(len(self.wolves), len(self.deer))
        
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

    def getNeighborhood(self, coords, size):
        
        neighborhood = []
        xlow = coords[0] - size
        if xlow < 0:
            xlow = 0
        xhi = coords[0] + size
        if xhi > c.MAPSIZE[0]-1:
            xhi = c.MAPSIZE[0]-1
        ylow = coords[1] - size
        if ylow < 0:
            ylow = 0
        yhi = coords[1] + size
        if yhi > c.MAPSIZE[1]-1:
            yhi = c.MAPSIZE[1]-1
        n = self.map[xlow:xhi+1]
        neighborhood = []
        for col in n:
            neighborhood.append(col[ylow:yhi+1])

        return neighborhood

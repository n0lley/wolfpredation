import numpy as np
import constants as c
import tile

class Wolf:
    
    def __init__(self, coords):
    
        self.coords = coords
        self.energy = 100
        self.heading = [np.random.random(),np.random.random()]
        
    def move(self, neighborhood):
    
        selfx = self.coords[0]
        selfy = self.coords[1]
        
        wolfheading = [0,0]
        closestDeer = [c.WOLFSENSERADIUS + 1, c.WOLFSENSERADIUS + 1]
        deerHeading = [0,0]
        
        #average heading of nearby wolves, biased towards the nearest deer.
        for col in neighborhood:
            for tile in col:
                
                if tile.id == "wolf" and tile.animal.coords != self.coords:
                    wolfheading[0] += tile.animal.heading[0]
                    wolfheading[1] += tile.animal.heading[1]
                
                if tile.id == "deer":
                    dist = abs(selfx - tile.coords[0]) + abs(selfy - tile.coords[1])
                    if dist < (abs(selfx - closestDeer[0]) + abs(selfy - closestDeer[1])):
                        closestDeer = tile.coords
                        deerHeading = [selfx-tile.coords[0], selfy-tile.coords[1]]
                    
        if abs(wolfheading[0]) + abs(wolfheading[1]) != 0:
            wolfheading[0] = wolfheading[0]/(abs(wolfheading[0]) + abs(wolfheading[1]))
            wolfheading[1] = wolfheading[1]/(abs(wolfheading[0]) + abs(wolfheading[1]))
        
        self.heading[0] += deerHeading[0]*2 + wolfheading[0]
        self.heading[1] += deerHeading[1]*2 + wolfheading[1]
        
        if self.heading[0]<0:
            xdir = -1
        elif self.heading[0]>0:
            xdir = 1
        else:
            xdir = 0
        if self.heading[1]<0:
            ydir = -1
        elif self.heading[1]>0:
            ydir = 1
        else:
            ydir = 0
  
        if selfx==0 and xdir==-1:
            xdir = np.random.choice([0,1])
            self.heading[0]*=-1
        elif selfx==c.MAPSIZE[0]-1 and xdir==1:
            xdir = np.random.choice([-1,0])
            self.heading[0]*=-1
        if selfy==0 and ydir==-1:
            ydir = np.random.choice([0,1])
            self.heading[1]*=-1
        elif selfy==c.MAPSIZE[1]-1 and ydir==1:
            selfy = np.random.choice([0,-1])
            self.heading[1]*=-1
         
        self.coords[0] += xdir
        self.coords[1] += ydir
        
    def eat(self, neighborhood):
    
        prey = None
        
        for col in neighborhood:
            for tile in col:
                if tile.id == "deer":
                    prey = tile.coords
                    break
        
        return prey
    
    def reproduce(self, neighborhood):
    
        
        return 0

import numpy as np
import constants as c
import tile

class Wolf:
    
    def __init__(self, ww=3, dw=5, energy=79, heading=[1,1]):
    
        self.wolfweight = ww
        self.deerweight = dw
        self.energy = energy
        self.heading = heading
        
    def move(self, coords, neighborhood):
    
        selfx = coords[0]
        selfy = coords[1]
        
        wolfheading = [0,0]
        closestDeer = [c.WOLFSENSERADIUS + 1, c.WOLFSENSERADIUS + 1]
        deerHeading = [0,0]
        
        #average heading of nearby wolves, biased towards the nearest deer.
        for col in neighborhood:
            for tile in col:
                
                if tile.id == "wolf":
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
        
        self.heading[0] += (deerHeading[0]*self.deerweight + wolfheading[0]*self.wolfweight)*1./3.
        self.heading[1] += (deerHeading[1]*self.deerweight + wolfheading[1]*self.wolfweight)*1./3.
        
        if self.heading[0] != 0 and self.heading[1] != 0:
            self.heading[0] /= (abs(self.heading[0]) + abs(self.heading[1]))
            self.heading[1] /= (abs(self.heading[0]) + abs(self.heading[1]))
        
        if self.heading[0]<0:
            xdir = self.heading[0] * c.WOLFSPEED
        elif self.heading[0]>0:
            xdir = self.heading[0] * c.WOLFSPEED
        else:
            xdir = 0
        if self.heading[1]<0:
            ydir = self.heading[1] * c.WOLFSPEED
        elif self.heading[1]>0:
            ydir = self.heading[1] * c.WOLFSPEED
        else:
            ydir = 0
        
        selfx += xdir
        selfy += ydir
        
        if selfx < 0:
            selfx = c.MAPSIZE[0]-1
        elif selfx > c.MAPSIZE[0]-1:
            selfx = 0
        if selfy < 0:
            selfy = c.MAPSIZE[1]-1
        elif selfy > c.MAPSIZE[1]-1:
            selfy = 0
        
        return int(selfx), int(selfy)
        
    def eat(self, neighborhood):
    
        prey = None
        
        for col in neighborhood:
            for tile in col:
                if tile.id == "deer":
                    prey = tile.coords
                    break
        
        return prey
    
    def reproduce(self, coords, neighborhood):
    
        chance1 = False
        chance2 = False
        babywolf = None
    
        for col in neighborhood:
            for tile in col:
                if tile.id == "wolf" and tile.coords != list(coords):
                    chance1 = True
                    break
          
        if chance1:
            for col in neighborhood:
                for tile in col:
                    if tile.id == "empty":
                        chance2 = True
                        coords = tile.coords
                        break
        
        if chance1 and chance2:
            self.energy /= 2
            babywolf = Wolf(energy=self.energy, heading=self.heading)
            
        return babywolf, (coords[0], coords[1])

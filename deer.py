import numpy as np
import constants as c

class Deer:
    
    def __init__(self, coords):
    
        self.coords = coords
        self.energy = 100
        self.heading = [np.random.random(), np.random.random()]
        
    def move(self, neighborhood):
        selfx = self.coords[0]
        selfy = self.coords[1]
        
        #check neighborhood. Run from wolves, follow deer.
        for col in neighborhood:
            for tile in col:
                if tile.id == "wolf":
                    dx = selfx - tile.coords[0]
                    dy = selfy - tile.coords[1]
                    self.heading[0] += dx/(abs(dx)+abs(dy))
                    self.heading[1] += dy/(abs(dx)+abs(dy))
                
                elif tile.id == "deer" and tile.animal.coords != self.coords:
                    self.heading[0] += tile.animal.heading[0]
                    self.heading[1] += tile.animal.heading[1]
        
        #normalize the heading
        if self.heading[0] + self.heading[1] != 0:
            self.heading[0] = self.heading[0]/(abs(self.heading[0])+abs(self.heading[1]))
            self.heading[1] = self.heading[1]/(abs(self.heading[0])+abs(self.heading[1]))
        
        #modify the weights to be biased towards heading
        xweights = [1./3., 1./3., 1./3.]
        yweights = [1./3., 1./3., 1./3.]
        if self.heading[0] < 0:
            xweights[0] += (1./6.) * abs(self.heading[0])
            xweights[1] = (1-xweights[0])/2
            xweights[2] = (1-xweights[0])/2
        else:
            xweights[2] += (1./6.) * self.heading[0]
            xweights[1] = (1-xweights[2])/2
            xweights[0] = (1-xweights[2])/2
            
        if self.heading[1] < 0:
            yweights[0] += (1./6.) * abs(self.heading[1])
            yweights[1] = (1-yweights[0])/2
            yweights[2] = (1-yweights[0])/2
        else:
            yweights[2] += (1./6.) * abs(self.heading[1])
            yweights[1] = (1-yweights[2])/2
            yweights[0] = (1-yweights[2])/2
            
        #don't go off the edge of the map
        if selfx == c.MAPSIZE[0]-1:
            xweights[0] += xweights[2]/2
            xweights[1] += xweights[2]/2
            xweights[2] = 0
        elif selfx == 0:
            xweights[2] += xweights[0]/2
            xweights[1] += xweights[0]/2
            xweights[0] = 0
            
        if selfy == c.MAPSIZE[1]-1:
            yweights[0] += yweights[2]/2
            yweights[1] += yweights[2]/2
            yweights[2] = 0
        elif selfy == 0:
            yweights[2] += yweights[0]/2
            yweights[1] += yweights[0]/2
            yweights[0] = 0
            
        #pick a direction
        xdir = np.random.choice([-1,0,1], p=xweights)
        ydir = np.random.choice([-1,0,1], p=yweights)
        
        self.coords[0] += xdir
        self.coords[1] += ydir
        
        if self.coords[0] < 0 or self.coords[0] >= c.MAPSIZE[0] or self.coords[0] < 0 or self.coords[0] >= c.MAPSIZE[1]:
            print(self.coords)

    
    def eat(self, neighborhood):
         print("TODO")
     
    def reproduce(self, neighborhood):
         print("TODO")

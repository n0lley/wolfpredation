import numpy as np
import constants as c
import tile

class Wolf:
    
    def __init__(self, coords):
    
        self.coords = coords
        self.energy = 100
        self.heading = [0,0]
        
    def move(self, neighborhood):
    
        selfx = self.coords[0]
        selfy = self.coords[1]
        
        closestDeer = [c.WOLFSENSERADIUS + 1, c.WOLFSENSERADIUS + 1]
        deerHeading = [0,0]
        
        #average heading of nearby wolves, biased towards the nearest deer.
        for col in neighborhood:
            for tile in col:
                
                if tile.id == "wolf":
                    self.heading[0] += tile.animal.heading[0]
                    self.heading[1] += tile.animal.heading[1]
                
                if tile.id == "deer":
                    dist = abs(selfx - tile.coords[0]) + abs(selfy - tile.coords[1])
                    if dist < (abs(selfx - closestDeer[0]) + abs(selfy - closestDeer[1])):
                        closestDeer = tile.coords
                        deerHeading = [(selfx-tile.coords[0])/dist, (selfy-tile.coords[1])/dist]
                    
        self.heading[0] += deerHeading[0]
        self.heading[1] += deerHeading[1]
        
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

    def eat(self, neighborhood):

        print("TODO")
        return 0
    
    def reproduce(self, neighborhood):
    
        print("TODO")
        return 0

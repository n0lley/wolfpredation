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
                    self.heading[0] += dx/(abs(dx)+abs(dy))*6
                    self.heading[1] += dy/(abs(dx)+abs(dy))*6
                
                elif tile.id == "deer" and tile.animal.coords != self.coords:
                    self.heading[0] += tile.animal.heading[0]
                    self.heading[1] += tile.animal.heading[1]
                    
        self.heading[0]/=abs(self.heading[0])
        self.heading[1]/=abs(self.heading[1])
        
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
        
        if self.coords[0] < 0 or self.coords[0] >= c.MAPSIZE[0] or self.coords[0] < 0 or self.coords[0] >= c.MAPSIZE[1]:
            print(self.coords)

    
    def eat(self, tile):
         
         self.energy += tile.energy
         tile.energy = 0
     
    def reproduce(self, neighborhood):
         print("TODO")

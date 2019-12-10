import numpy as np
import constants as c

class Deer:
    
    def __init__(self, ww=np.random.randint(10), dw=np.random.randint(10), energy=100, heading=[np.random.random(),np.random.random()]):
    
        self.wolfweight = ww
        self.deerweight = dw
        self.energy = energy
        self.heading = heading
        
    def move(self, coords, neighborhood):
        selfx = coords[0]
        selfy = coords[1]
        
        #check neighborhood. Run from wolves, follow deer.
        for col in neighborhood:
            for tile in col:
                if tile.id == "wolf":
                    dx = selfx - tile.coords[0]
                    dy = selfy - tile.coords[1]
                    self.heading[0] += dx/(abs(dx)+abs(dy))*self.wolfweight
                    self.heading[1] += dy/(abs(dx)+abs(dy))*self.wolfweight
                
                elif tile.id == "deer" and tile.coords != list(coords):
                    dx = selfx - tile.coords[0]
                    dy = selfy - tile.coords[1]
                    self.heading[0] += dx/(abs(dx)+abs(dy))*self.deerweight
                    self.heading[1] += dy/(abs(dx)+abs(dy))*self.deerweight
               
        if self.heading[0] != 0:
            self.heading[0]/=abs(self.heading[0])
        if self.heading[1] != 0:
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
            selfx = c.MAPSIZE[0]
        elif selfx==c.MAPSIZE[0]-1 and xdir==1:
            selfx = -1
        if selfy==0 and ydir==-1:
            selfy = c.MAPSIZE[1]
        elif selfy==c.MAPSIZE[1]-1 and ydir==1:
            selfy = 0
        
        selfx += xdir
        selfy += ydir
            
        return selfx, selfy
    
    def eat(self, tile):
         
         self.energy += tile.energy
         tile.energy = 0
     
    def reproduce(self, neighborhood):
         print("TODO")

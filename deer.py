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
        wolfheading = [0,0]
        deerheading = [0,0]
        for col in neighborhood:
            for tile in col:
                if tile.id == "wolf":
                    dx = selfx - tile.coords[0]
                    dy = selfy - tile.coords[1]
                    wolfheading[0] += dx
                    wolfheading[1] += dy
                
                elif tile.id == "deer" and tile.coords != list(coords):
                    deerheading[0] += tile.animal.heading[0]
                    deerheading[1] += tile.animal.heading[1]
        
        self.heading[0] += wolfheading[0]*self.wolfweight + deerheading[0]*self.deerweight
        self.heading[1] += wolfheading[1]*self.wolfweight + deerheading[1]*self.deerweight
        
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
     
    def reproduce(self, coords, neighborhood):
    
        chance1 = False
        chance2 = False
        babydeer = None
    
        for col in neighborhood:
            for tile in col:
                if tile.id == "deer" and tile.coords != list(coords):
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
            ww = self.wolfweight + np.random.choice([-1,0,1])
            dw = self.deerweight + np.random.choice([-1,0,1])
            babydeer = Deer(ww=ww, dw=dw, energy=self.energy, heading=self.heading)
            
        return babydeer, (coords[0], coords[1])

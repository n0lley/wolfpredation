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
        for col in neighborhood:
            for tile in col:
                
                if tile.id == "wolf":
                    self.heading[0] += tile.animal.heading[0]
                    self.heading[1] += tile.animal.heading[1]
                
                if tile.id == "deer":
                    print("deer")

    def eat(self, neighborhood):

        print("TODO")
        return 0
    
    def reproduce(self, neighborhood):
    
        print("TODO")
        return 0

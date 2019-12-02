import numpy as np
from copy import deepcopy

class Tile:

    def __init__(self, coords):
        
        self.id = "empty"
        self.animal = None
        self.energy = np.random.randint(0,100)
        self.coords = coords

    def addAnimal(self, animal):
        
        self.animal = deepcopy(animal)

import random
from mesa import Agent


class DrosselSchwabl(Agent):
    '''
    A forest-fire model cell based on the model of Drossel and Schwabl, 1992.
    
    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "On Fire", or "Burned Out"
        unique_id: (x,y) tuple. 
    
    unique_id isn't strictly necessary here, but it's good practice to give one to each
    agent anyway.
    '''
    def __init__(self, model, pos, tree):
        '''
        Create a new tree.
        Args:
            pos: The tree's coordinates on the grid. Used as the unique_id
        '''
        super().__init__(pos, model)
        self.pos = pos
        self.unique_id = pos
        self.condition = "Fine" if tree else "Empty"
        self.p = 0.1
        self.f = 0.1
    
    def set_on_fire(self):
        if self.condition == "Fine":
            self.condition = "On Fire"
        
    def step(self):
        '''
        If the tree is on fire, spread it to fine trees nearby.
        '''
        if self.condition == "Empty":
            if random.random() < self.p:
                self.condition = "Fine"

        if self.condition == "On Fire":
            neighbors = self.model.grid.get_neighbors(self.pos, moore=False)
            for neighbor in neighbors:
                neighbor.set_on_fire()
            self.condition = "Burned Out"
        
        if self.condition == "Fine":
            if random.random() < self.f:
                self.condition = "On Fire"
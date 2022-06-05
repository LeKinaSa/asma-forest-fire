import random
from mesa import Agent


class DrosselSchwabl(Agent):
    '''
    A forest-fire model cell based on the model of Drossel and Schwabl, 1992.
    
    Attributes:
        x, y: Grid coordinates
        condition: Can be "Empty", "Protected", "Fine", "On Fire", or "Burned Out"
        unique_id: (x,y) tuple.
        forest_density: density of the forest.
        protection: density of the protection systems in the forest.
        p: probability of growing a tree on an empty space.
        f: probability of a tree catching fire without having a burning neighbor.
    
    unique_id isn't strictly necessary here, but it's good practice to give one to each agent anyway.
    '''
    def __init__(self, model, pos, forest_density, protection, p, f):
        '''
        Create a new tree.
        Args:
            pos: The tree's coordinates on the grid. Used as the unique_id
        '''
        super().__init__(pos, model)
        self.pos = pos
        self.unique_id = pos
        
        random_value = random.random()
        self.condition = "Empty"
        if random_value < forest_density:
            self.condition = "Fine"
        if random_value > 1 - protection:
            self.condition = "Protected"
        
        self.last_condition = self.condition
        self.advance = True
        self.p = p
        self.f = f

    def set_on_fire(self):
        if self.condition == "Fine":
            self.condition = "On Fire"
    
    def step(self):
        '''
        Advance 1 step in the simulation.
        '''
        if self.advance:
            self.advance_step()
        else:
            self.estabilize_step()
        self.advance = not self.advance

    def advance_step(self):
        '''
        If the cell is empty, grow a tree with probability p.
        If the tree is on fire, spread it to fine trees nearby.
        If the tree is fine, catch fire with probability f.
        '''
        if (self.last_condition == "Empty" or self.last_condition == "Burned Out") and random.random() < self.p:
            self.condition = "Fine" # An empty space fills with a tree with probability p

        if self.last_condition == "On Fire":
            neighbors = self.model.grid.get_neighbors(self.pos, moore=False)
            for neighbor in neighbors:
                neighbor.set_on_fire() # A tree will burn if at least one neighbor is burning
            self.condition = "Burned Out" # A burning cell turns into an empty cell
        
        if self.last_condition == "Fine" and random.random() < self.f:
            self.condition = "On Fire" # A tree ignites with probability f even if no neighbor is burning
    
    def estabilize_step(self):
        '''
        Estabilize tree condition so the fire only spreads once every "step" (in this case, it will be once every 2 steps).
        '''
        self.last_condition = self.condition

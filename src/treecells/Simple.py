import random

from mesa import Agent


class Simple(Agent):
    '''
    A simple tree cell.
    
    Attributes:
        x, y: Grid coordinates
        condition: Can be "Empty", "Protected", "Fine", "On Fire", or "Burned Out"
        unique_id: (x,y) tuple.
        forest_density: density of the forest.
        protection: density of the protection systems in the forest.
    
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

        # Set all trees in the first column on fire.
        if self.pos[0] == 0:
            self.set_on_fire()
    
    def set_on_fire(self):
        if self.condition == "Fine":
            self.condition = "On Fire"

    def step(self):
        '''
        If the tree is on fire, spread it to fine trees nearby.
        '''
        if self.condition == "On Fire":
            neighbors = self.model.grid.get_neighbors(self.pos, moore=False)
            for neighbor in neighbors:
                neighbor.set_on_fire()
            self.condition = "Burned Out"

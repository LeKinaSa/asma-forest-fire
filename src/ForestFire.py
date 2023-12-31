from mesa import Model
from mesa.time import RandomActivation
from mesa.space import Grid
from mesa.datacollection import DataCollector

class ForestFire(Model):
    '''
    Simple Forest Fire model.
    '''
    def __init__(self, width, height, density, protection, TreeCell, p, f):
        '''
        Create a new forest fire model.
        
        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        '''
        # Initialize model parameters
        self.width = width
        self.height = height
        self.density = density
        self.protection = protection if protection != None else 1-density
        self.p = p
        self.f = f
        
        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(width, height, torus=False)
        self.dc = DataCollector({"Fine": lambda m: self.count_type(m, "Fine"),
                                 "On Fire": lambda m: self.count_type(m, "On Fire"),
                                 "Burned Out": lambda m: self.count_type(m, "Burned Out")})
        
        # Place a tree in each cell with Prob = density
        for x in range(self.width):
            for y in range(self.height):
                # Create a tree
                new_tree = TreeCell(self, (x, y), self.density, self.protection, self.p, self.f)
                self.grid[x][y] = new_tree
                self.schedule.add(new_tree)
        self.running = True
        self.steps = 0
        
    def step(self):
        '''
        Advance the model by one step.
        '''
        self.schedule.step()
        self.dc.collect(self)
        # Halt if no more fire or too much iterations
        if self.count_type(self, "On Fire") == 0 or self.steps > 250:
            self.running = False
        self.steps += 1
    
    @staticmethod
    def count_type(model, tree_condition):
        '''
        Helper method to count trees in a given condition in a given model.
        '''
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count

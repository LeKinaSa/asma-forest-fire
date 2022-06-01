from mesa import Agent


class SingleSpread(Agent):
    '''
    A tree cell.
    
    Attributes:
        x, y: Grid coordinates
        condition: Can be "Empty", "Fine", "On Fire", or "Burned Out"
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
        self.last_condition = self.condition
        self.advance = True
    
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

    def advance_step(self):
        '''
        If the tree is on fire, spread it to fine trees nearby.
        Only spread the fire if the tree has caught fire the last "step" (advance step).
        '''
        if self.last_condition == "On Fire":
            neighbors = self.model.grid.get_neighbors(self.pos, moore=False)
            for neighbor in neighbors:
                neighbor.set_on_fire()
            self.condition = "Burned Out"
        self.advance = False
    
    def estabilize_step(self):
        '''
        Estabilize tree condition so the fire only spreads once every "step" (in this case, it will be once every 2 steps).
        '''
        self.last_condition = self.condition
        self.advance = True

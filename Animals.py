import random
from CellWorld import *
from World import Animal, Interpreter
from Sensory import *
from Behaviors import *

class Turmite(Animal):
    """Represents a Turmite (see http://en.wikipedia.org/wiki/Turmite).

    Attributes:
        dir: direction, one of [0, 1, 2, 3]
        behavior: a Behavior (see Behaviors.py)
        pocket: a dictionary of possessions (with multiplicities)
    """

    def __init__(self, world, x=0, y=0, behavior=langton_ant, pocket=dict()):
        Animal.__init__(self, world, x, y)
        self.dir = 0
        self.pocket = pocket
        self.behavior = behavior
        self.draw()

    def draw(self):
        """Draw the Turmite."""
        # get the bounds of the cell
        cell = self.get_cell()
        bounds = self.world.cell_bounds(self.x, self.y)

        # draw a triangle inside the cell, pointing in the appropriate direction.
        # fill the triangle in with green if the animal is alive, with red if it is dead.
        bounds = rotate(bounds, self.dir)
        mid = vmid(bounds[1], bounds[2])
        if self.alive:
            self.tag = self.world.canvas.polygon([bounds[0], mid, bounds[3]], fill='green yellow')
        if not self.alive:
            self.tag = self.world.canvas.polygon([bounds[0], mid, bounds[3]], fill='red')

    def get_cell(self):
        #get the cell this turmite is on (creating one if necessary)
        x, y, world = self.x, self.y, self.world
        return world.get_cell(x,y) or world.make_cell(x,y)

    def step(self):
        self.behavior(self)


class Dustmite(Turmite):
    def __init__(self, world, x=0, y=0, behavior=eat_dust, pocket=dict(energy=0)):
        Turmite.__init__(self, world, x, y, behavior=behavior, pocket=pocket)

    def eat_dust(self): # Each dust eaten gives the mite 2 energy.
        cell = self.get_cell()
        shade = cell.shade
        if (shade > 0):
            self.pocket['energy'] += 2
            cell.change_shade(shade - 1)

    def use_energy(self):
        if self.pocket['energy'] == 0:
            self.die()
        else:
            self.pocket['energy'] -= 1


class Sensemite(Dustmite):
    def __init__(self, world, x=0, y=0, behavior=eat_dust, pocket=dict(energy=0), vision=None, hearing=None, touch=None, taste=None, smell=None):
        Dustmite.__init__(self, world, x, y, behavior=behavior, pocket=pocket)
        self.vision = vision
        self.hearing = hearing
        self.touch = touch
        self.taste = taste
        self.smell = smell
        self.senses = dict(sees=None, hears=None, feels=None, tastes=None, smells=None)


class Seemite(Sensemite):
    def __init__(self, world, x=0, y=0, behavior=greedy_eat_dust, pocket=dict(energy=0), vision=see):
        Sensemite.__init__(self, world, x, y, behavior=behavior, pocket=pocket, vision=vision)

    #----------------------------------------------------
    #Sensory functions
    def see(self):
        return self.vision(self, 1)

    #----------------------------------------------------
    #Cognition for utilizing the information gathered
    def choose_action(self):
        vision_field = self.see()
        self_coords = self.get_cell().indices
        choices = []
        max = 0
        for vision_coords in vision_field:
            vision_coords_as_neighborhood = [vision_coords]
            global_coords = local_to_global(vision_coords_as_neighborhood, self)[0]
            cell_data = {'vision_coords': vision_coords, 'dust': self.world.get_cell(global_coords[0], global_coords[1]).shade}
            if cell_data['dust'] >= max:
                if cell_data['dust'] > max:
                    choices = []
                choices.append(cell_data['vision_coords'])
                max = cell_data['dust']
        #Choose a random destination from equally preferable choices.
        chosen = random.choice(choices)
        return rot_of(chosen)







# The following are some useful vector operations
def vadd(p1, p2):
    """Adds vectors p1 and p2 (returns a new vector)."""
    return [x+y for x,y in zip(p1, p2)]

def vscale(p, s):
    """Multiplies p by a scalar (returns a new vector)."""
    return [x*s for x in p]

def vmid(p1, p2):
    """Returns a new vector that is the pointwise average of p1 and p2."""
    return vscale(vadd(p1, p2), 0.5)

def rotate(v, n=1):
    """Rotates the elements of a sequence by (n) places.
    Returns a new list.
    """
    n %= len(v)
    return v[n:] + v[:n]

# Additional Helper functions
def rot_of(chosen):
    if chosen[0] == 0 and chosen[1] == 0:
        rot = stay
        moving = False
    if chosen[0] == 0 and chosen[1] == 1:
        rot = stay
        moving = True
    if chosen[0] == 1 and chosen[1] == 0:
        rot = rt
        moving = True
    if chosen[0] == -1 and chosen[1] == 0:
        rot = lt
        moving = True
    if chosen[0] == 0 and chosen[1] == -1:
        rot = rev
        moving = True
    return (rot, moving)

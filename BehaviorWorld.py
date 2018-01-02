"""This module is part of Swampy, a suite of programs available from
allendowney.com/swampy.

Copyright 2011 Allen B. Downey
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import os
from PIL import Image
from Tkinter import END
from CellWorld import *
from World import Animal, Interpreter
from Behaviors import *
from WorldConfigs import *

class TurmiteWorld(CellWorld):
    """Provides a grid of cells that Turmites occupy."""

    def __init__(self, topology='infinite-plane', world_length=200, world_width=200, cell_size=10, canvas_size=600, default_behavior=collect_dust, configuration=blank_config, name='test', backup=True):
        CellWorld.__init__(self, topology, world_length, world_width, canvas_size, cell_size)
        self.default_behavior = default_behavior
        self.configuration = configuration
        self.name = name
        self.title(self.name)
        self.backup = backup
        
        # the interpreter executes user-provided code
        self.inter = Interpreter(self, globals())
        self.setup()

    def setup(self):
        """Makes the GUI."""
        self.row()
        self.make_canvas()

        # right frame
        self.col([0,0,1,0])

        self.row([1,1,1,1])
        self.bu(text='Make Turmite', command=self.make_turmite)
        self.bu(text='Make Dustmite', command=self.make_dustmite)
        self.bu(text='Print canvas', command=self.canvas.dump)
        self.bu(text='Quit', command=self.quit)
        self.endrow()

        # make the run and stop buttons
        self.row([1,1,1,1], pady=30)
        self.bu(text='Run', command=self.run)
        self.bu(text='Stop', command=self.stop)
        self.bu(text='Step', command=self.step)
        self.bu(text='Clear', command=self.clear)
        self.endrow()

        # create the text entry for adding code
        self.te_code = self.te(height=20, width=40)

        self.bu(text='Run code', command=self.run_text)
        self.endcol()

        #create a directory in sims devoted to this simulation
        self.sim_dir = "./sims/" + self.name
        if not os.path.exists(self.sim_dir):
            os.makedirs(self.sim_dir)
        else:
            print('A simulation by this name already exists. No new directory was created.')

    def save(self):
        file_name = self.name + "_" + str(self.time) + ".eps"
        file_path = self.sim_dir + "/" + file_name
        self.canvas.dump(file_path)

    def step(self):
        if (self.time == 0):
            self.save()
        """Invoke the step method on every animal. Then save the configuration."""
        for animal in self.animals:
            animal.step()
        self.time += 1
        if (self.backup==True):
            self.save()

    def make_turmite(self):
        """Makes a turmite."""
        turmite = Turmite(self, self.default_behavior)
        return turmite

    def make_dustmite(self):
        """Makes a dustmite."""
        dustmite = Dustmite(self)
        return dustmite

    def clear(self):
        """Removes all the animals and all the cells."""
        for animal in self.animals:
            animal.undraw()
        for cell in self.cells.values():
            cell.undraw()
        self.animals = []
        self.cells = {}

class Turmite(Animal):
    """Represents a Turmite (see http://en.wikipedia.org/wiki/Turmite).

    Attributes:
        dir: direction, one of [0, 1, 2, 3]
        behavior: a Behavior (see Behaviors.py)
        pocket: a dictionary of possessions (with multiplicities)
    """
    
    def __init__(self, world, behavior=langton_ant, pocket=dict()):
        Animal.__init__(self, world)
        self.dir = 0
        self.pocket = pocket
        self.behavior = behavior
        self.draw()

    def draw(self):
        """Draw the Turmite."""
        # get the bounds of the cell
        cell = self.get_cell()
        bounds = self.world.cell_bounds(self.x, self.y)

        # draw a triangle inside the cell, pointing in the
        # appropriate direction
        bounds = rotate(bounds, self.dir)
        mid = vmid(bounds[1], bounds[2])
        self.tag = self.world.canvas.polygon([bounds[0], mid, bounds[3]], fill='red')

    def get_cell(self):
        #get the cell this turmite is on (creating one if necessary)
        x, y, world = self.x, self.y, self.world
        return world.get_cell(x,y) or world.make_cell(x,y) 

    def step(self):
        self.behavior(self)


class Dustmite(Turmite):
    def __init__(self, world, behavior=collect_dust, pocket=dict(dust=0)):
        Turmite.__init__(self, world, behavior, pocket)

    def get_dust(self):
        cell = self.get_cell()
        shade = cell.shade
        if (shade > 0):
            self.pocket['dust'] += 1
            cell.change_shade(shade - 1)

# the following are some useful vector operations

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


if __name__ == '__main__':
    world = TurmiteWorld()
    world.mainloop()

world = TurmiteWorld('torus', 50, 50, cell_size=8, canvas_size=1000, configuration=random_shades_config, backup=False)
t = Dustmite(world, collect_dust)
"""This module is part of Swampyer, a suite of programs edited by Leland Reardon from the Swampy module, available from
allendowney.com/swampy.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import os
from PIL import Image
from Tkinter import END
from CellWorld import *
from World import Animal, Interpreter
from Animals import *
from Sensory import *
from Behaviors import *
from WorldConfigs import *

class BehaviorWorld(CellWorld):
    """Provides a grid of cells that Turmites occupy."""

    def __init__(self, topology='infinite-plane', world_length=200, world_width=200, cell_size=10, canvas_size=600, default_behavior=eat_dust, configuration=fifty_dustmites_random_on_random_shades, name='test', backup=True):
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
        file_name = self.name + "-" + str(self.time) + ".eps"
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
        turmite = Turmite(self, behavior=self.default_behavior)
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

#world = BehaviorWorld('torus', 20, 20, cell_size=8, canvas_size=1000, configuration=ten_dustmites_random_on_random_shades, name='10-mites-random-shades-20x20', backup=True)
#small_world = BehaviorWorld('torus', 5, 5, cell_size=15, canvas_size=1000, configuration=ten_dustmites_random_on_random_shades, name='10-mites-random-shades-5x5', backup=True)

if __name__ == '__main__':
    world = BehaviorWorld()
    world.mainloop()

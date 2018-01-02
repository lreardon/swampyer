"""This module is part of Swampy, a suite of programs available from
allendowney.com/swampy.

Copyright 2011 Allen B. Downey
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import math
import types
from World import World
from Cells import *
from WorldConfigs import *
import Tkinter
from Tkinter import N, S, E, W, VERTICAL, HORIZONTAL


class CellWorld(World):
    """Contains cells and animals that move between cells."""
    def __init__(self, topology='infinite-plane', world_width=50, world_length=50, canvas_size=500, cell_size=5, configuration=blank_config, interactive=False):
        World.__init__(self)
        self.title('CellWorld')
        self.topology = topology
        self.world_width = world_width
        self.world_length = world_length
        self.canvas_size = canvas_size
        self.cell_size = cell_size    
        self.configuration = configuration

        # cells is a map from index tuples to Cell objects
        self.cells = {}

        if interactive:
            self.make_canvas()
            self.make_control()

    def top_modulus(self, i, j):
        """Interprets the coordinates (i,j),
        according to the topology of the canvas of the world."""
        if (self.topology == 'infinite-plane'):
            return (i,j)
        if (self.topology == 'infinite-ribbon'):
            if abs(j) >= self.world_length:
                print('Cell coordinates outside range.')
                return None
            else:
                return (i,j)
        if (self.topology == 'rectangle'):
            if ((abs(i) >= self.world_width) or (abs(j) >= self.world_length)):
                print('Cell coordinates outside range.')
            else:
                return (i, j)
        if (self.topology == 'infinite-cylinder'):
            if (abs(i) >= self.world_width):
                i_mod = ((i + world_width) % (2 * self.world_width + 1)) - self.world_width
            return (i_mod, j)
        if (self.topology == 'finite-cylinder'):
            if (abs(j) >= self.world_length):
                print('Cell coordinates outside range.')
                return None
            i_mod = ((i + self.world_width) % (2 * self.world_width + 1)) - self.world_width
            return (i_mod, j)
        if (self.topology == 'torus'):
            i_mod = ((i + self.world_width) % (2 * self.world_width + 1)) - self.world_width
            j_mod = ((j + self.world_length) % (2 * self.world_length + 1)) - self.world_length
            return (i_mod, j_mod)

    def make_canvas(self):
        """Creates the GUI."""
        self.canvas = self.ca(width=self.canvas_size, 
                              height=self.canvas_size,
                              bg='white',
                              scale = [self.cell_size, self.cell_size])
        self.yb = self.sb(command=self.canvas.yview, sticky=N+S)
        self.yb.grid(row=0, column=1)
        self.xb = self.sb(command=self.canvas.xview, orient='horizontal', sticky=E+W)
        self.xb.grid(row=1, column=0)
        self.canvas.grid(row=0, column=0)
        self.canvas.configure(xscrollcommand=self.xb.set,
                              yscrollcommand=self.yb.set,
                              scrollregion=(0,0,self.world_width*self.cell_size,self.world_length*self.cell_size))
        self.configuration(self)

    def make_control(self):
        """Adds GUI elements that allow the user to change the scale."""

        self.la(text='Click or drag on the canvas to create cells.')
        self.row([0,1,0])
        self.la(text='Cell size: ')
        self.cell_size_en = self.en(width=10, text=str(self.cell_size))
        self.bu(text='resize', command=self.rescale)
        self.endrow()

    def bind(self):
        """Creates bindings for the canvas."""
        self.canvas.bind('<ButtonPress-1>', self.click)
        self.canvas.bind('<B1-Motion>', self.click)

    def click(self, event):
        """Event handler for clicks and drags.

        It creates a new cell or toggles an existing cell.
        """
        # convert the button click coordinates to an index tuple
        x, y = self.canvas.invert([event.x, event.y])
        i, j = int(math.floor(x)), int(math.floor(y))

        # toggle the cell if it exists; create it otherwise
        cell = self.get_cell(i,j)
        if cell:
            cell.toggle()
        else:
            self.make_cell(x, y)

    def make_cell(self, i, j, cell=None):
        """Creates and returns a new cell at i,j."""
        i_mod, j_mod = self.top_modulus(i, j)
        if (cell == None):
            cell = BoolCell(self, i_mod, j_mod)
        self.cells[i,j] = cell
        return cell

    def cell_bounds(self, i, j):
        """Return the bounds of the cell with indices i, j."""
        i_mod, j_mod = self.top_modulus(i, j)
        p1 = [i_mod, j_mod]
        p2 = [i_mod+1, j_mod]
        p3 = [i_mod+1, j_mod+1]
        p4 = [i_mod, j_mod+1]
        bounds = [p1, p2, p3, p4]
        return bounds

    def get_cell(self, i, j, default=None):
        """Gets the cell at i, j or returns the default value."""
        i_mod, j_mod = self.top_modulus(i, j)
        cell = self.cells.get((i_mod, j_mod), default)
        return cell

    four_neighbors = [(1,0), (-1,0), (0,1), (0,-1)]
    eight_neighbors = four_neighbors + [(1,1), (1,-1), (-1,1), (-1,-1)]

    def get_four_neighbors(self, cell, default=None):
        """Return the four Von Neumann neighbors of a cell."""
        return self.get_neighbors(cell, default, CellWorld.four_neighbors)
        
    def get_eight_neighbors(self, cell, default=None):
        """Returns the eight Moore neighbors of a cell."""
        return self.get_neighbors(cell, default, CellWorld.eight_neighbors)
        
    def get_neighbors(self, cell, default=None, deltas=[(0,0)]):
        """Return the neighbors of a cell.

        Args:
           cell: Cell
           deltas: a list of tuple offsets.
        """
        i, j = cell.indices
        cells = [self.get_cell(self.top_modulus(i+di, j+dj), default) for di, dj in deltas]
        return cells
        
    def rescale(self):
        """Event handler that rescales the world.

        Reads the new scale from the GUI,
        changes the canvas transform, and redraws the world.
        """
        cell_size = self.cell_size_en.get()
        cell_size = int(cell_size)
        self.canvas.transforms[0].scale = [cell_size, cell_size]
        self.redraw()

    def redraw(self):
        """Clears the canvas and redraws all cells and animals."""
        self.canvas.clear()
        for cell in self.cells.itervalues():
            cell.draw()
        for animal in self.animals:
            animal.draw()
            

if __name__ == '__main__':
    world = CellWorld(interactive=True)
    world.bind()
    world.mainloop()
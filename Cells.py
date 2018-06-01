"""
The concept of a cell has been generalized.
Allen Downey's Cell class is reformulated as BoolCell,
a sublcass of the abstract class Cell,
which has no speficied representation properties.
"""
class Cell(object):
    """A rectangular region in CellWorld"""
    def __init__(self, world, i, j):
        self.world = world
        self.pre_indices = i, j
        self.indices = self.world.top_modulus(i, j)
        self.bounds = self.world.cell_bounds(i, j)
        """
        The options attribute varies from cell type to cell type.
        It is overwritten in subclasses of Cell.
        """
        self.options = {}

    """
    The following method is used to initialize the cell's options.
    When called, it displays the cell in the world according to certain properties.
    It is overwritten in subclasses of Cell.
    """
    def set_options(self):
        return {}

    def draw(self):
        # bounds returns all four corners, so slicing every other
        # element yields two opposing corners, which is what we
        # pass to Canvas.rectangle
        coords = self.bounds[::2]
        self.item = self.world.canvas.rectangle(coords, **self.options)

    def undraw(self):
        """Delete any items with this cell's tag."""
        self.item.delete()
        self.item = None

    def get_config(self, option):
        """Gets the configuration of this cell."""
        return self.item.cget(option)

    def config(self, **options):
        """Configure this cell with the given options."""
        self.item.config(**options)

    def get_neighbors(self):
        indices = self.indices


# BoolCells can either be marked or unmarked.
class BoolCell(Cell):
    """A rectangular region in CellWorld"""
    def __init__(self, world, i, j, marked=False):
        Cell.__init__(self, world, i, j)
        self.marked = marked

        # Options configurations, which are chosen depending on marked.
        self.marked_options = dict(fill='black', outline='gray80')
        self.unmarked_options = dict(fill='yellow', outline='gray80')

        # self.options initialization for BoolCell.
        self.set_options()
        self.draw()

    # Define set_options for BoolCell
    def set_options(self):
        if (self.is_marked):
            self.options = self.marked_options
        else:
            self.options = self.unmarked_options
        return self.options

    """
    Additional methods for BoolCell.
    """
    def mark(self):
        """Marks this cell."""
        self.marked = True
        self.config(**self.marked_options)

    def unmark(self):
        """Unmarks this cell."""
        self.marked = False
        self.config(**self.unmarked_options)

    def is_marked(self):
        """Checks whether this cell is marked."""
        return self.marked

    def toggle(self):
        """Toggles the state of this cell."""
        if self.is_marked():
            self.unmark()
        else:
            self.mark()


# GrayCell can have one of 256 different shades, ranging from 0 to 255.
class GrayCell(Cell):
    def __init__(self, world, i, j, shade=0):
        Cell.__init__(self, world, i, j)
        self.shade = shade
        shade_hex_str_full = '0x{:02x}'.format(self.shade)
        shade_hex_str = shade_hex_str_full[2:]
        # A derived attribute of shade.
        self.shade_hex = '#' + (shade_hex_str*3)

        # An options configuration detremined by shade.
        self.shade_options = dict(fill=self.shade_hex, outline='black')

        # Initialize self.options for GrayCell
        self.set_options()
        self.draw()

    # Define set_options for GrayCell.
    def set_options(self):
         self.options = self.shade_options
         return self.options

    """
    Additional methods for GrayCell.
    """
    def get_shade(self):
        return self.shade

    def get_color(self):
        return self.shade_hex

    def change_shade(self, new_shade):
        self.shade = new_shade
        shade_hex_str_full = '0x{:02x}'.format(self.shade)
        shade_hex_str = shade_hex_str_full[2:]
        self.shade_hex = '#' + (shade_hex_str*3)
        self.shade_options = dict(fill=self.shade_hex, outline='black')
        self.set_options()
        self.config(**self.options)

class ColorCell(Cell):
    def __init__(self, world, i, j, r=0, g=0, b=0):
        Cell.__init__(self, world, i, j)
        self.r = r
        self.g = g
        self.b = b
        #Derived attributes of r, g, b.
        self.rgb = (self.r, self.g, self.b)
        self.color_hex = '#%02x%02x%02x' % self.rgb

        #An options configuration determined by color_hex.
        self.color_options = dict(fill=self.color_hex, outline='gray80')

        #self.options initialization for ColorCell
        self.set_options()
        self.draw()

    # Define set_options for ColorCell
    def set_options(self):
        self.options = self.color_options
        return self.options

    """
    Additional methods for ColorCell.
    """
    def get_rgb(self):
        return self.rgb

    def get_color(self):
        return self.color_hex

"""
Eventually it might be desirable to quickly generate cells with arbitrary parameters.
The following class will be used to do make that possible.
"""

class gCell(Cell):
    """
    A generator that returns a class generator for a cell with continuous and discrete properties,
    as well as a set_options method.
    The cell has no derived attributes, native options configurations, or additional methods.
    """
    def __init__(self, continuous, discrete):
        #continuous is a dictionary with keys as strings and values as real numbers.
        #discrete is a dictionary with keys as strings and values as integers.
        self.continuous = continuous
        self.discrete = discrete
    def __call__(self, world, i, j, set_options):
        g_cell = Cell(world, i, j)
        for parameter in self.continuous:
            g_cell.parameter = self.continuous[parameter]
        for parameter in self.discrete:
            g_cell.parameter = self.discrete[parameter]
        g_cell.set_options = types.MethodType(set_options, g_cell)
        return g_cell

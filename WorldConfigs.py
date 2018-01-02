from random import *
from Cells import *

class WorldConfig():
	def __init__(self, config_block):
		self.config_block = config_block
	def __call__(self, world):
		for i in range(-world.world_width,world.world_width+1):
			for j in range(-world.world_length, world.world_length+1):
				done = False
				for block in self.config_block:
					"""A function of i and j that returns a boolean value."""
					condition = block[0]
					"""The cell generator to call on world at i, j."""
					gen = block[1]
					"""Run the block."""
					if condition(i,j):
						done = True
						new_cell = gen(world, i, j)
					if (done == True):
						break
				if (done == False):
					new_cell = world.make_cell(i,j)
					new_cell.config(new_cell.options)

"""
Blocks are formatted as a sequence of pairs consisting of:
A function of i,j that returns a Boolean Value;
A function of world, i, j that creates a Cell at i,j in the specified world.
A function of 
"""

#All cells blank:
blank = [[lambda i,j: True, lambda world, i, j: 'yellow']]
blank_config = WorldConfig(blank)

#Checkerd:
checkered = [[lambda i,j: ((i+j)%2)==0, lambda world, i, j: Cell(world, i, j)],
			 [lambda i,j: True, 'yellow']]
checkered_config = WorldConfig(checkered)

#Random:
rand = [[lambda i,j: random() < 0.5, 'black'],
		  [lambda i,j: True, 'yellow']]
random_config = WorldConfig(rand)

#All cells are GrayCells, with randomly assigned shades:
random_shades = [
	[
		lambda i,j:
			True,
		lambda world, i, j:
			world.make_cell(i, j, GrayCell(world, i, j, randint(0,255)))
	]
]
random_shades_config = WorldConfig(random_shades)
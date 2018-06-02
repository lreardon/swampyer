from random import *
from Cells import *
from Animals import *
from Behaviors import *

class Config():
	def __init__(self, world_config, animals_config):
		self.world_config = world_config
		self.animals_config = animals_config
	def __call__(self, world):
		self.world_config(world)
		self.animals_config(world)


class WorldConfig():
	def __init__(self, w_config_blocks):
		self.w_config_blocks = w_config_blocks
	def __call__(self, world):
		for i in range(-world.world_width, world.world_width+1):
			for j in range(-world.world_length, world.world_length+1):
				done = False
				for block in self.w_config_blocks:
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

class AnimalsConfig():
	def __init__(self, a_config_blocks):
		self.a_config_blocks = a_config_blocks
	def __call__(self, world):
		for block in self.a_config_blocks:
			"""A condition of world that returns a boolean value."""
			condition = block[0]
			"""The animal generator, as a function of world."""
			gen = block[1]
			"""Run the generator until condition returns false."""
			while condition(world):
				gen(world)

#-------------------------------------------------------------------------------------------

# WORLD CONFIGURATIONS

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

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ANIMAL CONFIGURATIONS
#------------------------
def n_animals_random(animal, behavior, n):
	blocks = []
	animals_condition = lambda world: (len([a for a in world.animals if (a.__class__.__name__ == animal.__name__)]) < n)
	behavior = behavior
	place_mite = lambda world: animal(world=world, x=randint(-world.world_width, world.world_width+1), y=randint(-world.world_length, world.world_length+1), behavior=behavior)
	block = [animals_condition, place_mite]
	blocks.append(block)
	return blocks

def n_dustmites_random(n):
	blocks = []
	mites_condition = lambda world: (len([a for a in world.animals if (a.__class__.__name__ == Dustmite.__name__)]) < n)
	behavior = eat_dust
	place_mite = lambda world: Dustmite(world=world, x=randint(-world.world_width, world.world_width+1), y=randint(-world.world_length, world.world_length+1), behavior=behavior)
	block = [mites_condition, place_mite]
	blocks.append(block)
	return blocks

# Fifty dustmites are placed randomly throughout the world.
fifty_dustmites = n_dustmites_random(50)
fifty_dustmites_config = AnimalsConfig(fifty_dustmites)

# Ten dustmites are placed randomly throughout the world.
ten_dustmites = n_dustmites_random(10)
ten_dustmites_config = AnimalsConfig(ten_dustmites)

# Ten greedy dustmites are placed randomly throughout the world.
ten_greedy_dustmites = n_animals_random(Seemite, greedy_eat_dust, 10)
ten_greedy_dustmites_config = AnimalsConfig(ten_greedy_dustmites)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# CONFIGURATIONS
#----------------

fifty_dustmites_random_on_random_shades = Config(random_shades_config, fifty_dustmites_config)
ten_dustmites_random_on_random_shades = Config(random_shades_config, ten_dustmites_config)
ten_greedy_dustmites_random_on_random_shades = Config(random_shades_config, ten_greedy_dustmites_config)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#A running dictionary of all defined configurations, for use in Maingui
configurations = {'fifty_dustmites_random_on_random_shades':fifty_dustmites_random_on_random_shades, 'ten_dustmites_random_on_random_shades':ten_dustmites_random_on_random_shades, 'ten_greedy_dustmites_random_on_random_shades':ten_greedy_dustmites_random_on_random_shades}

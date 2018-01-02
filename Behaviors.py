#General static behavior class for simple automata,
#which can react to their environment according to
#if/then conditions.
from __future__ import print_function
from Motions import *
class Behavior():
	def __init__(self, blocks, **kwargs):
		self.blocks = blocks
		for (variable, assignment) in kwargs.items():
			variable = assignment

	def __call__(self, animal):
		done = False
		self.marker = 0
		while (not done):
			self.current_block = self.blocks[self.marker]
			if (self.current_block == 'END'):
				done = True
				break
			else:
				self.condition = self.current_block[0]
				self.actions = self.current_block[1]
				self.if_to = self.current_block[2]
				self.else_to = self.current_block[3]
				if (self.condition(animal)):
					for action in self.actions:
						action_receipt = action(animal)
						if (action_receipt == "!"):
							done = True
							break
					if (not done):
						self.marker = self.if_to
				else:
					self.marker = self.else_to
		self.animal=None

#A simple behavior.
langton_blocks = [
					[lambda animal: animal.get_cell().is_marked(), [lambda animal: lt(animal)], 2, 1],
					[lambda animal: True, [lambda animal: rt(animal)], 2, None],
					[lambda animal: True, [lambda animal: animal.get_cell().toggle()], 3, None],
					[lambda animal: True, [lambda animal: fd(animal)], 4, None],
					'END'
				]
langton_ant = Behavior(langton_blocks, cell=None)

gray_langton_blocks = [
					[lambda animal: animal.get_cell().shade > 127, [lambda animal: lt(animal)], 2, 1],
					[lambda animal: True, [lambda animal: rt(animal)], 2, None],
					[lambda animal: True, [lambda animal: animal.get_cell().change_shade(255-animal.get_cell().shade)], 3, None],
					[lambda animal: True, [lambda animal: fd(animal)], 4, None],
					'END'
				]
gray_langton_ant = Behavior(gray_langton_blocks, cell=None)

collect_dust_blocks = [
						[lambda animal: animal.get_cell().shade > 0, [lambda animal: animal.get_dust()], 1, 3],
						[lambda animal: animal.get_cell().shade > 127, [lambda animal: rt(animal)], 3, 2],
						[lambda animal: True, [lambda animal: lt(animal)], 3, None],
						[lambda animal: True, [lambda animal: fd(animal)], 4, None],
						'END'
					]
collect_dust = Behavior(collect_dust_blocks, cell=None)
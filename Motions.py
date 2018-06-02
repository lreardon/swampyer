#How animals can move throughout the grid.

#Two Component Motions
class DirectedTranslation():
	def __init__(self, trans_long, trans_lat):
		self.trans_long = trans_long
		self.trans_lat =trans_lat
	def __call__(self, animal):
		if (animal.dir==0):
			hyp_x = animal.x + self.trans_long
			hyp_y = animal.y - self.trans_lat
		elif (animal.dir==1):
			hyp_y = animal.y + self.trans_long
			hyp_x = animal.x + self.trans_lat
		elif (animal.dir==2):
			hyp_x = animal.x - self.trans_long
			hyp_y = animal.y + self.trans_lat
		else:
			hyp_y = animal.y - self.trans_long
			hyp_x = animal.x - self.trans_lat
		hyp_coords = animal.world.top_modulus(hyp_x, hyp_y)
		if (hyp_coords != None):
			animal.x, animal.y = hyp_coords
			return (animal.x, animal.y)
		else:
			print(str(animal) + ' wants to move beyond the world\'s boundaries. Held still.')
			return "!"

class Rotation():
	def __init__(self, rot):
		self.rot = rot
	def __call__(self, animal):
		animal.dir = (animal.dir+self.rot) % 4
		return animal.dir

#General Motion
class Motion():
	def __init__(self, trans_long, trans_lat, rot):
		self.trans_long = trans_long
		self.trans_lat = trans_lat
		self.rot = rot
	def __call__(self, animal):
		dt = DirectedTranslation(self.trans_long, self.trans_lat)
		dt_receipt = dt(animal)
		if (dt_receipt == "!"):
			return "!"
		r = Rotation(self.rot)
		r_receipt = r(animal)
		animal.redraw()
		return (dt_receipt, r_receipt)

#Some Simple Motions
def stay(animal):
	m = Motion(0,0,0)
	return m(animal)

def lt(animal):
	m = Motion(0,0,1)
	return m(animal)
def rt(animal):
	m = Motion(0,0,-1)
	return m(animal)
def rev(animal):
	m = Motion(0,0,2)
	return m(animal)

def fd(animal, dist=1):
	m = Motion(dist,0,0)
	return m(animal)
def bk(animal, dist=1):
	m = Motion(-dist,0,0)
	return m(animal)
def slr(animal, dist=1):
	m = Motion(0,dist,0)
	return m(animal)
def sll(animal, dist=1):
	m = Motion(0,-1,0)
	return m(animal)

#Abstract simple motions, parameterizable.
def fdk(k):
	return lambda animal: fd(animal, k)
def bkk(k):
	return lambda animal: bk(animal, k)
def slrk(k):
	return lambda animal: slr(animal, k)
def sllk(k):
	return lambda animal: sll(animal, k)

#Sensory Functions

def see(animal, n):
    animal_location = animal.get_cell().indices
    animal_neighborhood = get_neighborhood(animal_location[0], animal_location[1], n)
    animal.vision_field = global_to_local(animal_neighborhood, animal)
    return animal.vision_field










#-------------------------------------------------------------
#Helper Functions
def get_neighborhood(x,y,n):
    square = []
    neighborhood = []
    for i in range(-n,n+1):
        for j in range(-n, n+1):
                square.append((x+i, y+j))
    for coord in square:
        if (((x-coord[0])**2+(y-coord[1])**2)**0.5 <= n):
            neighborhood.append(coord)
    return neighborhood

def global_to_local(neighborhood, animal):
    local_origin = animal.get_cell().indices
    local_direction = animal.dir
    local_trans_neighborhood = [(cell[0] - local_origin[0], cell[1] - local_origin[1]) for cell in neighborhood]
    rotated = rotate_neighborhood(local_direction, local_trans_neighborhood)
    return rotated

def local_to_global(neighborhood, animal):
    direction_global = animal.dir
    inv_dir = (2 - direction_global) % 4
    global_rot_neighborhood = rotate_neighborhood(inv_dir, neighborhood)
    origin_global = animal.get_cell().indices
    translated = [(cell[0] + origin_global[0], cell[1] + origin_global[1]) for cell in global_rot_neighborhood]
    return translated

def rotate_neighborhood(dir, neighborhood):
    if dir == 0:
        rotated = [(-cell[1], cell[0]) for cell in neighborhood]
    if dir == 1:
        rotated = [(cell[0], cell[1]) for cell in neighborhood]
    if dir == 2:
        rotated = [(cell[1], -cell[0]) for cell in neighborhood]
    if dir == 3:
        rotated = [(-cell[0], -cell[1]) for cell in neighborhood]
    return rotated

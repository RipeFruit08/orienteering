from PIL import Image
import Terrain
import State
import heapq
import time
import sys
import Pixel

pix = None
elevations = []

"""
Generates successors for a given state.
In this situation, a state represents a cell on the map and therefore will have at most
8 different successors. This function calls MakeSuccessor which will handle invalid successors
(i.e. Successors that have x,y coordinate out of bounds or states with terrain out bounds)
:param: the state being used to generate successors
"""
def GetSuccessors(state):
	succ = []
	x = state.x
	y = state.y
	gX = state.goalX
	gY = state.goalY
	# successors to the right
	s = MakeSuccessor(x+1, y-1, gX, gY)
	if s != None: succ.append(s) 
	s = MakeSuccessor(x+1, y, gX, gY)
	if s != None: succ.append(s) 
	s = MakeSuccessor(x+1, y+1, gX, gY)
	if s != None: succ.append(s) 
	
	# above and below
	s = MakeSuccessor(x, y+1, gX, gY)
	if s != None: succ.append(s) 
	s = MakeSuccessor(x, y-1, gX, gY)
	if s != None: succ.append(s) 
	
	# successors to the left
	s = MakeSuccessor(x-1, y-1, gX, gY)
	if s != None: succ.append(s) 
	s = MakeSuccessor(x-1, y, gX, gY)
	if s != None: succ.append(s) 
	s = MakeSuccessor(x-1, y+1, gX, gY)
	if s != None: succ.append(s) 
	return succ

"""
Generates a successor based on x, y, gX, and gY
:param: x  the x coordinate of successor
:param: y  the y coorinaate of successor
:param: gX the x coordinate of the goal
:param: gY the y coordinate of the goal
:return: None if the x or y coordinates are invalid or if the terrain at that successor is out of bounds
         otherwise, State object representing the successor is return
"""
def MakeSuccessor(x,y, gX, gY):
	if (x < 0 or x >= MAX_X() or y < 0 or y >= MAX_Y()):
		return None
	ele = elevations[x][y]
	ter = Terrain.GetTerrainVal(pix[x,y])
	if ter == Terrain.OutOfBounds():
		return None
	s = State.State(ele,ter,x,y,gX,gY)
	return s

"""
Maximum x coordinate value
"""
def MAX_X():
	return 395

"""
Maximum y coordinate value
"""
def MAX_Y():
	return 500

"""
Checks if a State object, ele, is contained in a list of states, lst
:param: lst, the list of state objects
:param: ele, the state object in question
:return: True if ele is in lst, False otherwise
"""
def contains(lst, ele):
	for s in lst:
		if s.x == ele.x and s.y == ele.y:
			return True
	return False

"""
Runs A* search on an initial state, init
:param: init, the initial state
:return: a list of state objects leading from the goal to init
NOTE that the path that gets returned is in reverse order 
"""
def A_star(init):
	#a* search
	pq = []
	costs = {}
	visited = []
	print(init)
	costs[init] = 0
	heapq.heappush(pq, (init.priority, init))
	path = []
	parents = {}
	parents[init] = None
	while True:
		state = heapq.heappop(pq)[1]
		if (state.isGoal()):
			print("finished")
			# build path
			while(state != None):
				path.append(state)
				state = parents[state]
			return path
			break
		for s in GetSuccessors(state):
			if not contains(visited, s):
				#print(s)
				visited.append(s)
				speed = 1
				if (float(s.elevation) > float(state.elevation)):
					speed = float(s.elevation) / float(state.elevation) # slower uphill 
				# movement in the y direction
				if (s.x == state.x):
					costs[s] = costs[state] + (1/(s.terrain * speed))*Pixel.Latitude()
				# movement in the x direction
				elif (s.y == state.y):
					costs[s] = costs[state] + (1/(s.terrain * speed))*Pixel.Longitude()
				# otherwise, diagonal movement
				else:
					costs[s] = costs[state] + (1/(s.terrain * speed))*Pixel.Diag()
				heapq.heappush(pq, (costs[s] + s.priority, s))
				parents[s] = state		
	

"""
Takes a list of State objects, lst, and produces 'human readable' output to get 
from the first point to the last point
:param: lst, a list of State objects
:return: None, this function prints the human readable output
"""
def hr_output(lst, nth):
	prev = lst[0]
	dir = 0 # direction
	cnt = 0 # number of times to move in that direction
	for i in range(len(lst)-1):
		next = lst[i+1]
		# if x and y are changing -> moving diagonally
		if (prev.x != next.x and prev.y != next.y):
			# moving northwest
			if (next.x < prev.x and next.y > prev.y):
				tmp = 1
				if dir == tmp:
					cnt += 1
				else:
					hr_print(dir, cnt)
					cnt = 1
					dir = tmp
			# moving northeast 
			elif (next.x > prev.x and next.y > prev.y):
				tmp = 3
				if dir == tmp:
					cnt += 1
				else:
					# print out
					hr_print(dir, cnt)
					cnt = 1
					dir = tmp
			# moving southwest
			elif (next.x < prev.x and next.y < prev.y):
				tmp = 6
				if dir == tmp:
					cnt += 1
				else:
					# print out
					hr_print(dir, cnt)
					cnt = 1
					dir = tmp
			# moving southeast				
			elif (next.x > prev.x and next.y < prev.y):
				tmp = 8
				if dir == tmp:
					cnt += 1
				else:
					# print out
					hr_print(dir, cnt)
					cnt = 1
					dir = tmp

		# x stays the same -> moving latitudinally (up/down)
		elif (prev.x == next.x):
			# moving north
			if (next.y > prev.y):
				tmp = 2
				if dir == tmp:
					cnt += 1
				else:
					hr_print(dir,cnt)
					cnt = 1
					dir = tmp
			# moving south
			elif (next.y < prev.y):
				tmp = 7
				if dir == tmp:
					cnt += 1
				else:
					hr_print(dir,cnt)
					cnt = 1
					dir = tmp
		# y stays the same -> moving longitudinally (left/right)
		elif (prev.y == next.y):
			# moving east 
			if (next.x > prev.x):
				tmp = 5
				if dir == tmp:
					cnt += 1
				else:
					hr_print(dir,cnt)
					cnt = 1
					dir = tmp
			# moving west
			elif (next.x > prev.x):
				tmp = 4
				if dir == tmp:
					cnt += 1
				else:
					hr_print(dir,cnt)
					cnt = 1
					dir = tmp
		prev = next 
	print("Now at control " + str(nth))
	print()
			
"""
prints the 'direction' that you are moving based on dir, cnt
:param: dir integer (1-8) representing the direction you are moving
:param: cnt the number of units to move
:return: nothing, this function prints
"""
def hr_print(dir, cnt):
	# no direction was set
	if dir == 0:
		return
	str_dir, multiplier = get_direction(dir)
	print("Move " + str(round(multiplier * cnt,1)) + "m in " + str_dir)

"""
Returns the 'direction' that you are moving based on val
:param: val integer (1-8) representing what direction you are moving
"""
def get_direction(val):
	switcher = {
		1: ("Northwest", Pixel.Diag()),
		2: ("North", Pixel.Latitude()),
		3: ("Northeast", Pixel.Diag()),
		4: ("West", Pixel.Longitude()),
		5: ("East", Pixel.Longitude()),
		6: ("Southwest",Pixel.Diag()),
		7: ("South", Pixel.Latitude()),
		8: ("Southeast", Pixel.Diag())
	}
	
	return switcher.get(val)
"""
Update pixel mapping based on a particular season
:param: mode int representing which seasons
0 -> summer, no change necessary
1 -> fall, easy movement forests & adjacent cells become slightly harder
2 -> winter, all water that is within 7 pixels of non-water is now ice (slightly easier than rough meadow)
3 -> spring, any pixel within 15 pixels of water without gaining more than 1m in elevation is underwater
:return: nothing, this function modifies the global pixel array
"""
def change_season(mode):
	if (mode == 1):
		do_fall()
	elif (mode == 2):
		do_winter()
	elif (mode == 3):
		do_spring()
	else:
		return

"""
returns a list of tuples corresponding to the neighbors the tuple coord
:param: coord a tuple representing an x,y coordinate
:return: a list containing tuples representing all valid neighbors of coord
"""
def pixel_neighbors(coord):
	x, y = coord
	neighbors = []
	# neighbors to the right
	c = make_neighbor(x+1, y-1)
	if c != None: neighbors.append(c) 
	c = make_neighbor(x+1, y)
	if c != None: neighbors.append(c) 
	c = make_neighbor(x+1, y+1)
	if c != None: neighbors.append(c) 
	
	# neighbors above and below
	c = make_neighbor(x, y+1)
	if c != None: neighbors.append(c) 
	c = make_neighbor(x, y-1)
	if c != None: neighbors.append(c) 

	# neighbors to the left
	c = make_neighbor(x-1, y-1)
	if c != None: neighbors.append(c) 
	c = make_neighbor(x-1, y)
	if c != None: neighbors.append(c) 
	c = make_neighbor(x-1, y+1)
	if c != None: neighbors.append(c) 	
	return neighbors

"""
returns a tuple representing a coordinate that is not in the out of bounds cell
and has indices that are not out of bounds
:param: x an integer representing an x coordinate
:param: y an integer representing a  y coordinate
:return: a tuple, or None if the resulting tuple is invalid 
"""
def make_neighbor(x, y):
	# validates out of bound indices 
	if (x < 0 or x >= MAX_X() or y < 0 or y >= MAX_Y()):
		return None
	ter = Terrain.GetTerrainVal(pix[x,y])
	# filters out of bound neighbors
	if ter == Terrain.OutOfBounds():
		return None
	# must be a valid neighbor at this point
	return (x,y)

"""
Updates the global pixel array to compensate for the fall season
In the fall, easy movement forest and adjacent cells become harder to traverse
This simulates the fact that in the fall leaves fall obscuring paths
:return: None
"""
def do_fall():
	print("do fall was called")
	newColor = (128, 128, 128, 255)
	oldColor = (255,255,255,255) 
	print(Terrain.GetTerrainVal((255,255,255,255)))
	s = time.time()
	for x in range(MAX_X()):
		for y in range(MAX_Y()):
			if (pix[x,y] == oldColor):
				for tup in pixel_neighbors((x,y)):
					i, j = tup
					t_val = Terrain.GetTerrainVal(pix[i,j])
					if pix[i,j] != pix[x,y] and t_val != Terrain.Water() and t_val != Terrain.ImpassibleVeg() and t_val	!= Terrain.RoughMeadow():
						pix[i,j] = newColor
				pix[x,y] = newColor
	e = time.time()
	print(e - s)
	
"""
Updates the global pixel array to compensate for the winter season
In the winter, all water that is within 7 pixels of land becomes icy
In this implementation icy cells are treated to be about on par with
rough meadows in terms of difficulty. All qualifying cells turn light blue
"""
def do_winter():
	print("do winter was called")
	newColor = (113, 237, 255, 255)
	oldColor = (0,0,255,255)
	s = time.time() 
	for x in range(MAX_X()):
		for y in range(MAX_Y()):
			if (pix[x,y] == oldColor):  # found water
				ice_flag = False
				for tup in pixel_neighbors((x,y)):
					i,j = tup
					if (pix[i,j] != oldColor and pix[i,j] != newColor): # if any neighbor is land
						ice_flag = True
						break
				if (ice_flag): # make ice cells
					# DLT
					winter_DLT(x,y)
					pix[x,y] = newColor
	e = time.time()
	print(e-s)

"""
runs a Depth Limited Traversal from pixel at x,y coloring each
pixel visited light blue, stopping if a non water is seen or
if the depth is reached
:param: x the x coordinate of the originating cell
:param: y the y coordinate of the originating cell
:param: d the depth limited
"""	
def winter_DLT(x, y, d = 7):
	t_val = Terrain.GetTerrainVal(pix[x,y])
	if (t_val != Terrain.Water()):
		return
	if (d == 0):
		return
	pix[x,y] = (113, 237, 255, 255)
	for tup in pixel_neighbors((x,y)):
		i,j = tup
		winter_DLT(i,j, d-1)
		
def do_spring():
	print("spring was called")
	newColor = (113, 237, 255, 255)
	oldColor = (0,0,255,255)
	s = time.time() 
	for x in range(MAX_X()):
		for y in range(MAX_Y()):
			if (pix[x,y] == oldColor):  # found water
				underwater = False
				for tup in pixel_neighbors((x,y)):
					i,j = tup
					if (pix[i,j] != oldColor and pix[i,j] != newColor): # if any neighbor is land
						underwater = True
						break
				if (underwater): # make ice cells
					# DLT
					spring_DLT(x,y,float(elevations[y][x]))
					#pix[x,y] = newColor
	# bit of a hack, iterate through pixels again and change all "ice" to water to more
	# appropriately show that it is underwater
	for x in range(MAX_X()):
		for y in range(MAX_Y()):
			if (pix[x,y] == newColor):
				pix[x,y] = oldColor
					
	e = time.time()

def spring_DLT(x, y, base, d = 15):
	t_val = Terrain.GetTerrainVal(pix[x,y])
	e_val = float(elevations[y][x])
	diff = e_val - base	
	if (diff > 1):
		return
	if (d == 0):
		return
	pix[x,y] = (113, 237, 255, 255)
	for tup in pixel_neighbors((x,y)):
		i,j = tup
		t_val = Terrain.GetTerrainVal(pix[i,j])
		if (t_val != Terrain.Water() and t_val != Terrain.Ice()):
			spring_DLT(i,j, base, d-1)
			
def main():
	global pix
	global elevations
	img = Image.open('elevations_pixels.PNG')
	pix = img.load()
	with open('elevations.txt') as f:
		elevations = [ line.split() for line in f ]
	img.show()	
	#do_fall()
	#do_winter()
	#do_spring()
	#img.show()
	#return
	
	print("done")
	print(len(elevations))
	points = []
	if (len(sys.argv) > 2):
		print("argument was passed!")
		with open(sys.argv[1]) as f:
			points = [tuple([int(i) for i in line.split()]) for line in f]
		season = int(sys.argv[2])
		change_season(season)
		paths = []
		stime = time.time()
		for i in range(len(points)-1):
			start = points[i]
			end = points[i+1]
			init = State.State(elevations[start[0]][start[1]], Terrain.GetTerrainVal(pix[start[0],start[1]]), start[0], start[1], end[0], end[1])
			paths.append(A_star(init))
		etime = time.time()
		counter = 1
		for path in paths:
			path.reverse()
			hr_output(path, counter)
			counter += 1
			for s in path:
				pix[s.x,s.y] = (255,0,0,255)		
		print(etime - stime)
		img.show()
		img.close()
		#print(points)
	# no file parameter passed, defaults to using points for brown path
	else:
		print("Usage: python3 orienteering.py file [season mode bit]")
		print("\tSEASON MODE BITS")
		print("\t0 -> summmer")
		print("\t1 -> fall")
		print("\t2 -> winter")
		print("\t3 -> spring")
		points = [(230, 327),(276, 279),(303, 240),(306, 286),(290, 310),(304, 331),(306, 341),(253, 372),(246, 355),(288, 338),(282, 321),(243, 327),(230, 327)]
	
if __name__ == "__main__":
	main()
	

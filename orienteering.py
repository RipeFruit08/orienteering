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

def main():
	global pix
	global elevations
	img = Image.open('elevations_pixels.PNG')
	pix = img.load()
	with open('elevations.txt') as f:
		elevations = [ line.split() for line in f ]
	print("done")
	print(len(elevations))
	points = []
	if (len(sys.argv) > 1):
		print("argument was passed!")
		with open(sys.argv[1]) as f:
			points = [tuple([int(i) for i in line.split()]) for line in f]
		#print(points)
	# no file parameter passed, defaults to using points for brown path
	else:
		points = [(230, 327),(276, 279),(303, 240),(306, 286),(290, 310),(304, 331),(306, 341),(253, 372),(246, 355),(288, 338),(282, 321),(243, 327),(230, 327)]
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
	
if __name__ == "__main__":
	main()
	

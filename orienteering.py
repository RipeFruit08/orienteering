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
				# movement in the x direction
				if (s.x == state.x):
					costs[s] = costs[state] + (1/(s.terrain * speed))*Pixel.Longitude()
				# movement in the y direction
				elif (s.y == state.y):
					costs[s] = costs[state] + (1/(s.terrain * speed))*Pixel.Latitude()
				# otherwise, diagonal movement
				else:
					costs[s] = costs[state] + (1/(s.terrain * speed))*Pixel.Diag()
				heapq.heappush(pq, (costs[s] + s.priority, s))
				parents[s] = state
	#for state in path:
		#print(state)
		#pix[state.x,state.y] = (255,0,0,255)		
	

def main():
	global pix
	global elevations
	print('hello')
	img = Image.open('elevations_pixels.PNG')
	pix = img.load()
	print(pix)
	print(pix[0,0])
	print(pix[228,308])
	print(pix[230,327])
	#pix[168,236] = (255,0,0,255)
	#pix[178,222] = (255,0,0,255)
	#pix[0,0] = (0,0,0,255)
	#img.show()
	x = img.size[0]
	y = img.size[1]
	print(x)
	print(y)
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
	else:
		points = [(230, 327),(276, 279),(303, 240),(306, 286),(290, 310),(304, 331),(306, 341),(253, 372),(246, 355),(288, 338),(282, 321),(243, 327),(230, 327)]
	paths = []
	"""
	#init = State.State(elevations[168][236], Terrain.GetTerrainVal(pix[168,236]), 168, 236, 178, 222)
	init = State.State(elevations[230][327], Terrain.GetTerrainVal(pix[230,327]), 230, 327, 276, 279)
	start = time.time()
	paths.append(A_star(init))
	end = time.time()
	print(end-start)
	"""
	stime = time.time()
	for i in range(len(points)-1):
		start = points[i]
		end = points[i+1]
		init = State.State(elevations[start[0]][start[1]], Terrain.GetTerrainVal(pix[start[0],start[1]]), start[0], start[1], end[0], end[1])
		paths.append(A_star(init))
	etime = time.time()
	for path in paths:
		for s in path:
			pix[s.x,s.y] = (255,0,0,255)		
	print(etime - stime)
	img.show()
	img.close()
	
if __name__ == "__main__":
	main()
	

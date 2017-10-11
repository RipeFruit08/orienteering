from PIL import Image
import Terrain
import State
import heapq
import time
import sys

pix = None
elevations = []

def GetSuccessors(state):
	succ = []
	# successors above
	succ.append(State.State(elevations[state.x+1][state.y-1], Terrain.GetTerrainVal(pix[state.x+1,state.y-1]), state.x+1, state.y-1, state.goalX, state.goalY))
	succ.append(State.State(elevations[state.x+1][state.y], Terrain.GetTerrainVal(pix[state.x+1,state.y]), state.x+1, state.y, state.goalX, state.goalY))
	succ.append(State.State(elevations[state.x+1][state.y+1], Terrain.GetTerrainVal(pix[state.x+1,state.y+1]), state.x+1, state.y+1, state.goalX, state.goalY))
	succ.append(State.State(elevations[state.x][state.y-1], Terrain.GetTerrainVal(pix[state.x,state.y-1]), state.x, state.y-1, state.goalX, state.goalY))
	succ.append(State.State(elevations[state.x][state.y+1], Terrain.GetTerrainVal(pix[state.x,state.y+1]), state.x, state.y+1, state.goalX, state.goalY))
	succ.append(State.State(elevations[state.x-1][state.y-1], Terrain.GetTerrainVal(pix[state.x-1,state.y-1]), state.x-1, state.y-1, state.goalX, state.goalY))
	succ.append(State.State(elevations[state.x-1][state.y], Terrain.GetTerrainVal(pix[state.x+1,state.y]), state.x+1, state.y, state.goalX, state.goalY))
	succ.append(State.State(elevations[state.x-1][state.y+1], Terrain.GetTerrainVal(pix[state.x-1,state.y+1]), state.x-1, state.y+1, state.goalX, state.goalY))
	return succ

def contains(lst, ele):
	for s in lst:
		if s.x == ele.x and s.y == ele.y:
			return True
	return False

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
					speed = 0.8 # slower uphill 
				costs[s] = costs[state] + 1/(s.terrain * speed)
				heapq.heappush(pq, (costs[s] + s.priority, s))
				parents[s] = state
	#for state in path:
		#print(state)
		#pix[state.x,state.y] = (255,0,0,255)		
	
#230 327
#276 279
#303 240
#306 286
#290 310
#304 331
#306 341
#253 372
#246 355
#288 338
#282 321
#243 327
#230 327
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
	if (len(sys.argv) > 1):
		print("argument was passed!")
		return
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
	


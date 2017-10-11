import Pixel
"""
Class representing the state of each pixel.
This class contains information of its own terrain, elevation,
(x,y) coordinate and the coordinates of its goal state (goalX, goalY)
"""
class State:
	def __init__(self, elevation, terrain, x, y, goalX, goalY):
		self.elevation = elevation
		self.terrain = terrain
		self.x = x
		self.y = y
		self.goalX = goalX
		self.goalY = goalY
		self.priority = (((goalX - x)**2 + (goalY - y)**2 )**(1/2)) * Pixel.Diag()
		
	# for heap purposes
	def __lt__(other, self):
		if isinstance(other, self.__class__):
			return self.x < other.x
		return NotImplemented
		
	# checks if the state is goal
	def isGoal(self):
		return self.x == self.goalX and self.y == self.goalY
	
	# print function for debugging purposes	
	def __str__(self):
		return "this is a state at (" + str(self.x) + ", " + str(self.y) + ")"
		
if __name__ == "__main__":
	pass

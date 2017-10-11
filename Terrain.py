def OutOfBounds():
	return 0.0
	
def ImpassibleVeg():
	return 0.1
	
def Water():
	return 0.2
	
def RoughMeadow():
	return 0.3
	
def WalkForest():
	return 0.4
	
def EasyMovementForest():
	return 0.5
	
def SlowRunForest():
	return 0.6
	
def OpenLand():
	return 0.8
	
def Footpath():
	return 0.9	
	
def PavedRoad():
	return 1.0
	
def GetTerrainVal(color):
	switcher = {
		(248,148,18,255): OpenLand(),
		(255,192,0,255): RoughMeadow(),
		(255,255,255,255): EasyMovementForest(),
		(2,208,60,255): SlowRunForest(),
		(2,136,40,255): WalkForest(),
		(5,73,24,255): ImpassibleVeg(),
		(0,0,255,255): Water(),
		(71,51,3,255): PavedRoad(),
		(0,0,0,0): Footpath(),             # picture sometimes has this for black
		(0,0,0,255): Footpath(),           # and sometimes this for black 
		(205,0,101,255): OutOfBounds()
	}
	
	return switcher.get(color)
	
if __name__ == "__main__":
	print("test")


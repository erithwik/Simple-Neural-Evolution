import random
import numpy as np
import math
import time
import os

SIZE_X = 70
SIZE_Y = 13
COUNT_ANIMALS = 30
COUNT_FOOD = 70
LENGTH_OF_PARENT_POP = 10

class locationManager:
	def __init__(self, countAnimals, countFood, area):
		self.countFood = countFood
		self.countAnimals = countAnimals
		self.foods = []
		self.animals = []
		self.area = area

	def createInit(self):
		for i in range(0, self.countFood):
			randomX = random.randint(1, SIZE_X - 2)
			randomY = random.randint(1, SIZE_Y - 2)
			f = food(randomX, randomY)
			f.addToBoard(self.area)
			self.foods.append(f)

		for j in range(0, self.countAnimals):
			randomX = random.randint(2, SIZE_X - 2)
			randomY = random.randint(2, SIZE_Y - 2)
			a = animal(randomX, randomY, 0, 0)
			a.addToBoard(self.area)
			self.animals.append(a)
	
	def makeChild(self, animal1, animal2):
		animal1W1 = animal1.nn.W1.tolist()
		animal1W2 = animal1.nn.W2.tolist()
		animal2W1 = animal2.nn.W1.tolist()
		animal2W2 = animal2.nn.W2.tolist()
		childW1 = []
		childW2 = []
		for i in range(0, len(animal1W1)):
			tmp = []
			for j in range(0, len(animal1W1[i])):
				randomVal = random.randint(0,2)
				if(randomVal == 0):
					tmp.append(animal1W1[i][j])
				else:
					tmp.append(animal2W1[i][j])
			childW1.append(tmp)

		for i in range(0, len(animal1W2)):
			tmp = []
			for j in range(0, len(animal1W2[i])):
				randomVal = random.randint(0,2)
				if(randomVal == 0):
					tmp.append(animal1W2[i][j])
				else:
					tmp.append(animal2W2[i][j])
			childW2.append(tmp)

		randomX = random.randint(2, SIZE_X - 2)
		randomY = random.randint(2, SIZE_Y - 2)
		child = animal(randomX, randomY, np.array(childW1), np.array(childW2))
		return child
		# print(child)		

	def nextGen(self):
		fitness = []
		for i in range(0, len(self.animals)):
			if(self.animals[i] == 'dead'):
				continue
			fitness.append(self.animals[i].points)
		sortedFit = sorted(fitness, key=int, reverse=True)
		parentPop = self.arrangeTopVal(sortedFit[0:LENGTH_OF_PARENT_POP])

		print('This is the new ParentPop points')
		for i in range(0, len(parentPop)):
			print(str(parentPop[i].points))
		a = input('')

		for i in range(0, len(self.animals)):
			if(self.animals[i] == 'dead'):
				continue
			self.area.loc[self.animals[i].locY][self.animals[i].locX] = '.'
			self.animals[i] = 'dead'


		for i in range(self.countAnimals):
			firstLoc = random.randint(0, len(parentPop)-1)
			secondLoc = random.randint(0, len(parentPop)-1)

			child = self.makeChild(parentPop[firstLoc], parentPop[secondLoc])
			# print(' ')
			# print(parentPop[firstLoc])
			# print(parentPop[secondLoc])
			# print(' ')
			# print(child)
			self.animals.append(child)
			# print(child)
			# print(self.animals)
			# a = input("")


	def arrangeTopVal(self, fitnessList):
		newList = []
		for i in fitnessList:
			for j in range(0, len(self.animals)):
				if(self.animals[j] == 'dead'):
					continue
				if(self.animals[j].points == i):
					newList.append(self.animals[j])
					self.area.loc[self.animals[j].locY][self.animals[j].locX] = '.'
					self.animals[j] = 'dead'
					break
		return newList

	def mutate(self):
		a = 2

	def actualAction(self):
		for i in self.animals:
			if(i == 'dead'):
				continue
			i.move(self.foods, self.area)
			for j in range(0, len(self.foods)):
				if(self.foods[j] == 'empty'):
					continue
				if((i.locX == self.foods[j].locX) and (i.locY == self.foods[j].locY)):
					i.points += 1
					self.area.loc[self.foods[j].locY][self.foods[j].locX] = '.'
					self.foods[j] = 'empty' 

class gameManager:
	def __init__(self):
		self.area = location(SIZE_X, SIZE_Y)
		self.area.makeLoc()
		self.locManager = locationManager(COUNT_ANIMALS, COUNT_FOOD, self.area)
		self.locManager.createInit()
  
	def run(self, steps, generations):
		for i in range(0, generations):	
			# print(len(self.locManager.animals))
			# print(self.locManager.animals)
			#
			for j in range(0, steps):
				#os.system('cls')
				os.system('cls')
				self.locManager.actualAction()
				self.area.printLoc()
				time.sleep(.3)

			totalFoods = 0
			for i in range(0, len(self.locManager.foods)):
				if(self.locManager.foods[i] != 'empty'):
					totalFoods += 1
			print("How many foods are left: " + str(totalFoods))

			for i in range(0, len(self.locManager.animals)):
				if(self.locManager.animals[i] == 'dead'):
					continue
				print("Animal " + str(i) + " points: " + str(self.locManager.animals[i].points))
			a = input('')
			
			tmpFoodList = []
			for i in range(len(self.locManager.foods)):
				if(self.locManager.foods[i] == 'empty'):
					continue
				else:
					tmpFoodList.append(self.locManager.foods[i])

			if(len(tmpFoodList) <= COUNT_FOOD):
				for i in range(0, COUNT_FOOD - len(tmpFoodList)):
					randomX = random.randint(2, SIZE_X - 2)
					randomY = random.randint(2, SIZE_Y - 2)
					f = food(randomX, randomY)
					f.addToBoard(self.locManager.area)
					self.locManager.foods.append(f)

			print(len(self.locManager.foods))
			self.locManager.nextGen()


class neuralNetwork():
	def __init__(self, weights1, weights2):
		self.inputLayerSize = 2
		self.hiddenLayerSize = 7
		self.outputLayerSize = 4
    
		self.W1 = weights1
		self.W2 = weights2
		  
	def makeRandomWeights(self):
		self.W1 = np.random.randn(self.inputLayerSize, self.hiddenLayerSize)
		self.W2 = np.random.randn(self.hiddenLayerSize, self.outputLayerSize)
    
	def forward(self, X):
		self.z2 = np.dot(X, self.W1)
		self.a2 = self.activationFunction(self.z2)
		self.z3 = np.dot(self.a2, self.W2)
		output = self.activationFunction(self.z3)
		return output
	    
	def activationFunction(self, z):
		return 1/(1+np.exp(-z))
    
class location:
	def __init__(self, sizeX, sizeY):
		self.sizeX = sizeX
		self.sizeY = sizeY

	def makeLoc(self):
		self.loc = []
		for i in range(0, self.sizeY):
			tmp = []
			for j in range(0, self.sizeX):
				tmp.append('.')
			self.loc.append(tmp)

	def printLoc(self):
		for i in range(0, self.sizeY):
			for j in range(0, self.sizeX):
				print(self.loc[i][j], end = '')
			print("\n")

class animal:
	def __init__(self, locX, locY, weights1, weights2):
		self.characterType = 'O'
		self.locX = locX
		self.locY = locY
		
		self.points = 0
		
		self.nn = neuralNetwork(weights1, weights2)
		if(type(weights1) == int):
			self.nn.makeRandomWeights()

	def addToBoard(self, area):
		area.loc[self.locY][self.locX] = self.characterType
	
	def locationBetweenSpots(self, locX, locY):
		distX = self.locX - locX
		distY = self.locY - locY
		distTotal = math.pow(distX,2) + math.pow(distY,2)
		distTotal - math.sqrt(distTotal)
		return distTotal
	  
	def closestFood(self, listOfFood):
		lowestIndex = 0
		lowestDistance = 1000000
		for i in range(0, len(listOfFood)):
			if(listOfFood[i] == 'empty'):
				continue
			if(self.locationBetweenSpots(listOfFood[i].locX, listOfFood[i].locY) < lowestDistance):
				lowestDistance = self.locationBetweenSpots(listOfFood[i].locX, listOfFood[i].locY)
				lowestIndex = i
		xDist =listOfFood[lowestIndex].locX - self.locX
		yDist = listOfFood[lowestIndex].locY - self.locY
		return lowestIndex, xDist, yDist
	  
	def move(self, listOfFood, map):
		index, xDist, yDist = self.closestFood(listOfFood) # ******** Put xDist and yDist in a numpyArray **********
		inputDat = np.array([xDist, yDist], dtype = float) #Check if this is array or np array
		output = self.nn.forward(inputDat)
		output = output.tolist()
		greatestInd = self.greatestIndex(output)
		map.loc[self.locY][self.locX] = '.'
		if(greatestInd == 0): #MAKE SURE THIS IS RIGHT
			if(self.locX != 0):
				self.locX = self.locX - 1
			else:
				self.locX = self.locX
		elif(greatestInd == 1):
			if(self.locX != SIZE_X-1):
				self.locX = self.locX + 1
			else:
				self.locX = self.locX
		elif(greatestInd == 2):
			if(self.locY != 0):
				self.locY = self.locY - 1
			else:
				self.locY = self.locY
		else:
			if(self.locY != SIZE_Y-1):
				self.locY = self.locY + 1
			else:
				self.locY = self.locY
		self.addToBoard(map)

	
	def greatestIndex(self, list):
		greatestVal = -1000
		greatestInd = 0
		for i in range(0, len(list)):
			if(list[i] > greatestVal):
				greatestVal = list[i]
				greatestInd = i
		return greatestInd

class food:
	def __init__(self, locX, locY):
		self.characterType = '*'
		self.locX = locX
		self.locY = locY

	def addToBoard(self, area):
		area.loc[self.locY][self.locX] = self.characterType

game = gameManager()
game.run(20, 5)
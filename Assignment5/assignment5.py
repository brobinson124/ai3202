#Brooke Robinson
#Assignment 5
#Used Assignment 2 as a base
#Worked with Mario Alanis 


import sys

class Node:#node represent a grid squard
  
	def __init__(self, locationx, locationy, type_val):
		self.x = locationx 
		self.y = locationy
		self.p = None
		self.typeN = type_val #0 is free, 1 is mountain, 2 is wall, 3 is a snake, 4 is a barn
		if type_val == 0:#awards associated with each type value
			self.reward = 0 
		elif type_val == 1: #Mountain
			self.reward = -1
		elif type_val == 3: #Snake
			self.reward = -2
		elif type_val == 4: #Barn
			self.reward = 1
		elif type_val == 50: #the Apple!
			self.reward = 50
		else:
			self.reward = 0
	
	def setParent(self, parent): #setting the parent
		self.p = parent

def getMap(arg):
	mymap = []
	with open(arg, 'r') as f:
	  for line in f:
		line = line.strip()
		if len(line) > 0:
			mymap.append(map(int, line.split()))
	for x in (range(0,len(mymap))):
		for y in range(0,len(mymap[x])):
			mymap[x][y] = Node(x,y,int(mymap[x][y]))
			#print mymap[x][y].x,mymap[x][y].y, mymap[x][y].reward
	return mymap


class MDP:
	
	def __init__(self, mymap):
		self.Open = {}
		self.Close = {}
		self.mymap = mymap
		self.length = len(mymap)
		self.goal = mymap[0][9]
		self.start = mymap[7][0]
		self.util_list = {} #a list that stores the utilities for the current
		self.prev_util = {} #a list that stores the utilities for the previous
		
	def getAdj(self, n):
		#Added for MDP: No cornors
		adj_matrix = []
		for x in range(n.x-1, n.x+2): #we add +2 because the range does not include the final value
			for y in range(n.y-1, n.y+2):
				if(x>= 0 and  y>=0 and x<len(self.mymap) and y<len(self.mymap[x]) and not (x== n.x and y==n.y)):
					if not((x == n.x-1 and y == n.y-1) or (x==n.x+1 and y==n.y+1) or (x==n.x-1 and y ==n.y+1) or (n==n.x+1 and y==n.y-1)):
					#we have to make sure it is within bounds(No corners!)
					#we also have to make sure we do not add the same node
						if(self.mymap[x][y].reward != 2):
							adj = mymap[x][y]
							adj_matrix.append(adj)
							self.u = 0
		return adj_matrix
		
	def expect_u(self, e):#e=epsilon, our parameter
		
		#let's initialize all of our map to 0.0 reward
		for x in range(0,len(self.mymap)):
			for n in self.mymap[x]:
				self.util_list[n] = 0.0
				self.prev_util[n] = 0.0
		
		d = 1.0#d=delta, a way to measure our parameter
		
		while(d>(e*(1.0-0.9)/0.9)): #our parameters
			for x in range(0,len(self.mymap)):
				for node in self.mymap[x]:
					self.prev_util[node] = self.util_list[node] #add it to our previous to remember value for next loop
					max_val = self.MDPfunc(node) #find the policy with the max reward
					self.util_list[node] = node.reward +0.9*max_val #0.9 is our living reward
					if node.typeN == 2: #cannot be a wall
						self.util_list[node] = 0.0
						
			d = 0.0 #reset delta
			#we want to loop through the map in order to find if any of the nodes are greater than delta(our parameter tester)
			for x in range(0,len(self.mymap)):
				for node in self.mymap[x]:
					if abs(self.util_list[node] - self.prev_util[node]) > d: 
						d = abs(self.util_list[node] - self.prev_util[node]) #update our parameters	
		#print('\n'.join(['	'.join(['{0:.2f}'.format(self.util_list[item]) for item in row]) for row in self.mymap])) 
		#prints the grid of our utilities: I got this specifically from Mario in order to test my code

	def MDPfunc(self, n): 
		#Our policy-finding function
		adj = self.getAdj(n)
		stored_vals = []
		for val in adj:
			if val.x == n.x: #have to check up option and down option
				if val.y >= 0 and val.y < (len(self.mymap[0])-1): 
					if self.mymap[val.x][val.y+1] in adj:
						node1 = self.mymap[n.x][n.y+1]
					else:
						node1 = 0.0
					if self.mymap[n.x][n.y-1] in adj:
						node2 = self.mymap[n.x][n.y-1]
					else:
						node2 = 0.0
					if node1 == 0.0 and node2 == 0.0:
						stored_vals.append(0.8*self.prev_util[val])
					elif node1 == 0.0:
						stored_vals.append(0.8*self.prev_util[val]+0.1*(self.prev_util[node2]))
					elif node2 == 0.0:
						stored_vals.append(0.8*self.prev_util[val]+0.1*(self.prev_util[node1]))
					else:
						stored_vals.append(0.8*self.prev_util[val]+0.1*self.prev_util[node1]+0.1*self.prev_util[node2])
			elif val.y == n.y: #check left option and right option
				if val.x >= 0 and val.x < (len(self.mymap)-1):
					if self.mymap[val.x+1][val.y] in adj:
						node1 = self.mymap[n.x+1][n.y]
					else:
						node1 = 0.0
					if self.mymap[n.x-1][n.y] in adj:
						node2 = self.mymap[n.x-1][n.y]
					else:
						node2 = 0.0
					if node1 == 0.0 and node2 == 0.0:
						stored_vals.append(0.8*self.prev_util[val])
					elif node1 == 0.0:
						stored_vals.append(0.8*self.prev_util[val]+0.1*self.prev_util[node2])
					elif node2 == 0.0:
						stored_vals.append(0.8*self.prev_util[val]+0.1*self.prev_util[node1])
					else:
						stored_vals.append(0.8*self.prev_util[val]+0.1*self.prev_util[node1]+0.1*self.prev_util[node2])
					
		return max(stored_vals)	#return the best policy
		
		
	#A* search (Modified)
	def starsearch(self):
		self.Open[self.start] = self.util_list[self.start] #start our Open list with the reward value stored in util_list 
		while self.Open != {}:
			#find reward that is the LARGEST
			max_val_find = max(self.Open, key=self.Open.get)#we want the largest reward, so I changed MIN to MAX
			max_val = self.Open[max_val_find]
			for value in self.Open:
				if self.Open[value] == max_val:
					node = value
					break
			del self.Open[node]
			if node.x == self.goal.x and node.y == self.goal.y:
				self.time_to_print(node)
				break
		
			self.Close[node] = self.util_list[node]
			node_adj = self.getAdj(node)
			for n in node_adj:
				if (n.typeN != 2 and not(n in self.Close)):
					if not(n in self.Open) or (self.util_list[n] > self.util_list[node]):
						n.setParent(node)
						if not(n in self.Open):
							self.Open[n] = self.util_list[n]
		
	
	def time_to_print(self, nextNode):
		print "This is my path: "
		cost = 0
		stringArr = []
		while not(nextNode.x == self.start.x and nextNode.y == self.start.y):
			stringArr.append(["(", nextNode.x, ",", nextNode.y, ")","Utility: ",self.util_list[nextNode]])
			nextNode = nextNode.p
		stringArr.append(["(", nextNode.x, ",", nextNode.y, ")", "Utility: ",self.util_list[nextNode]])
		for lis in reversed(stringArr):
			print lis[0],lis[1],lis[2],lis[3],lis[4],lis[5],lis[6]
		

mymap = getMap(sys.argv[1])
searched = MDP(mymap)
searched.expect_u(float(sys.argv[2]))
searched.starsearch()


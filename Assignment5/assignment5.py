#Brooke Robinson
#Assignment 5
#Used Assignment 2 as a base
#Worked with Mario Alanis 
import sys
import math

class Node:
  
	def __init__(self, locationx, locationy, typeN):
		self.x = locationx 
		self.y = locationy
		self.p = None
		self.f = 0
		self.cost = 0
		self.typeN = typeN #0 is free, 1 is mountain, 2 is wall
	
	def setParent(self, parent, h):
		self.p = parent
		self.cost = parent.cost + 10 + int(self.x != parent.x and self.y !=parent.y)*4 + self.typeN*10
		self.f = self.cost + h(self.x, self.y)

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
			#print mymap[x][y].x,mymap[x][y].y, mymap[x][y].typeN
	return mymap

def newCost(n, node):
	return 10 + int(n.x != node.x and n.y != node.y)*4 + n.typeN*10

class astar:
	
	def __init__(self, mymap, heuristic):
		#self.Open = []
		self.Open = {}
		self.Close = {}
		self.mymap = mymap
		self.length = len(mymap)
		self.goal = mymap[0][9]
		self.start = mymap[7][0]
		if heuristic == 1:
			self.h = self.man
		else:
			self.h = self.pyth
		
	def getAdj(self, n):
		adj_matrix = []
		for x in range(n.x-1, n.x+2): #we add +2 because the range does not include the final value
			for y in range(n.y-1, n.y+2):
				if(x>= 0 and  y>=0 and x<len(self.mymap) and y<len(self.mymap[x]) and not (x== n.x and y==n.y)):
					#we have to make sure it is within bounds
					#we also have to make sure we do not add the same node
					if(self.mymap[x][y].typeN != 2):
						adj = mymap[x][y]
						adj_matrix.append(adj)
		return adj_matrix
		
	def man(self,x,y):
		man_val = abs(x-self.goal.x) + abs(y-self.goal.y)
		return man_val
	
	def pyth(self, x, y):
		#use the a^2 + b^2 = c^2 theory!
		return math.sqrt((((x-self.goal.x)**2) + ((y-self.goal.y)**2)))
		
	#A* search!	
	def starsearch(self):
		locations = 0
		node = self.start
		self.Open[node] = node.f 
		while self.Open != {}:
			locations = locations + 1
			#find node.f that is the smallest
			min_val_find = min(self.Open, key=self.Open.get)
			min_val = self.Open[min_val_find]
			for value in self.Open:
			#	print "In Open: ", val.x, val.y, val.f
				if self.Open[value] == min_val:
					node = value
					break
			#		print "min_val", min_val
			#print "remove: ", node.f
			#self.Open.remove(node)
			del self.Open[node]
			if node.x == self.goal.x and node.y == self.goal.y:
				#print "goal: ", self.goal.x, " ",self.goal.y
				#print "current: ", node.x, node.y
				#print "p of current: ", node.p.x, node.p.y
				#print "Locations evaluated: ", locations
				self.time_to_print(node)
				break
				
			#print "*********************"
			#print "Adding to close: (", node.x, ", ",node.y,")"
			#print "*********************"
			
			self.Close[node] = node.f
			node_adj = self.getAdj(node)
			for n in node_adj:
				if (n.typeN != 2 and not(n in self.Close)):
					if not(n in self.Open) or (n.f > (node.f + newCost(n,node))):
						n.f = node.f + newCost(n,node)
						n.setParent(node,self.h)#calculates the f value
						if not(n in self.Open):
							self.Open[n] = n.f
							#print "adding to open: ", n.x, n.y
	
	def time_to_print(self, nextNode):
		print "This is my path: "
		cost = 0
		stringArr = []
		while not(nextNode.x == self.start.x and nextNode.y == self.start.y):
			#print "(", nextNode.x, ",", nextNode.y, ")"
			stringArr.append(["(", nextNode.x, ",", nextNode.y, ")"])
			cost += newCost(nextNode, nextNode.p)
			nextNode = nextNode.p
		stringArr.append(["(", nextNode.x, ",", nextNode.y, ")"])
		for lis in reversed(stringArr):
			print lis[0],lis[1],lis[2],lis[3],lis[4]
		print "Total Cost: ", cost
		
		


mymap = getMap(sys.argv[1])
searched = astar(mymap, int(sys.argv[2]))
searched.starsearch()


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
		self.typeN = typeN #0 is free, 1 is mountain, 2 is wall, 3 is a snake, 4 is a barn
	
	def setParent(self, parent):
		self.p = parent
		if self.typeN == 0:
			type_val = 0
		if self.typeN == 1:
			type_val = -1
		if self.typeN == 3:
			type_val = -2
		if self.typeN == 4:
			type_val = 1
		self.cost = parent.cost + 10 + int(self.x != parent.x and self.y !=parent.y)*4 + type_val
		self.f = self.cost 

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
	return 1
	#return 10 + int(n.x != node.x and n.y != node.y)*4 + n.typeN*10

class MDP:
	
	def __init__(self, mymap, e):
		#self.Open = {}
		#self.Close = {}
		self.mymap = mymap
		self.length = len(mymap)
		self.goal = mymap[0][9]
		self.start = mymap[7][0]
		self.e = e
		self.u = 0
		
	def getAdj(self, n):
		adj_matrix = []
		#our A* found adjs in the corners
		#we do not want corners this time
		for x in range(n.x-1, n.x+2): #we add +2 because the range does not include the final value
			for y in range(n.y-1, n.y+2):
				if(x>= 0 and  y>=0 and x<len(self.mymap) and y<len(self.mymap[x]) and not (x== n.x and y==n.y)):
					if not((x == n.x-1 and y == n.y-1) or (x==n.x+1 and y==n.y+1) or (x==n.x-1 and y ==n.y+1) or (n==n.x+1 and y==n.y-1)):
					#we have to make sure it is within bounds(No corners!)
					#we also have to make sure we do not add the same node
						if(self.mymap[x][y].typeN != 2):
							adj = mymap[x][y]
							adj_matrix.append(adj)
							self.u = 0
		return adj_matrix
		
	def MDPfunc(self):
		gama = 0.9
		#R(s) = reward of state 
		#using Bellman equation for utilities
			#U(s) = R(s) + gama*argmax * sum(P(s' given s,a)*U(s'))
			#ex) U(3,1) = R(3,1)+gama*max{.8U(2,1)+.1U(3,2)+.1U(3,1),.9U(3,1)+...}
			
			
		
		

	'''	
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
				if self.Open[value] == min_val:
					node = value
					break
			del self.Open[node]
			if node.x == self.goal.x and node.y == self.goal.y:
				#self.time_to_print(node)
				break
		
			self.Close[node] = node.f
			node_adj = self.getAdj(node)
			for n in node_adj:
				if (n.typeN != 2 and not(n in self.Close)):
					if not(n in self.Open) or (n.f > (node.f + newCost(n,node))):
						#n.f = node.f + newCost(n,node)
						#n.setParent(node,self.h)#calculates the f value
						if not(n in self.Open):
							self.Open[n] = n.f
							#print "adding to open: ", n.x, n.y
		'''
	
	def time_to_print(self, nextNode):
		print "This is my path: "
		cost = 0
		stringArr = []
		while not(nextNode.x == self.start.x and nextNode.y == self.start.y):
			#print "(", nextNode.x, ",", nextNode.y, ")"
			stringArr.append(["(", nextNode.x, ",", nextNode.y, ")"])
			#cost += newCost(nextNode, nextNode.p)
			nextNode = nextNode.p
		stringArr.append(["(", nextNode.x, ",", nextNode.y, ")"])
		for lis in reversed(stringArr):
			print lis[0],lis[1],lis[2],lis[3],lis[4]
		print "Total Cost: ", cost
		
		


mymap = getMap(sys.argv[1])
searched = MDP(mymap, sys.argv[2])
searched.starsearch()


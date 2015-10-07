#Brooke Robinson
#Assignment 5
#Used Assignment 2 as a base
#Worked with Mario Alanis 
import sys
#import math

class Node:
  
	def __init__(self, locationx, locationy, type_val):
		self.x = locationx 
		self.y = locationy
		self.p = None
		self.u = 0
		self.typeN = type_val
		#self.cost = 0
		#self.type_val = type_val #0 is free, 1 is mountain, 2 is wall, 3 is a snake, 4 is a barn
		if type_val == 0:
			self.reward = 0
		elif type_val == 1:
			self.reward = -1
		elif type_val == 3:
			self.reward = -2
		elif type_val == 4:
			self.reward = 1
		elif type_val == 50:
			self.reward = 50
		else:
			self.reward = 0
	
	def setParent(self, parent):
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
		self.util_list = {}
		
	def getAdj(self, n):
		adj_matrix = []
		#our A* found adjs in the corners
		#we do not want corners this time
		#print "test:", n.y
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
		
	def expect_u(self, e):#e=epsilon
		d = 1.0#sigma
		
		while(d>(e*(1.0-0.9)/0.9)): #our parameters
			for x in range(0,len(self.mymap)):
				for node in self.mymap[x]:
					max_val = self.MDPfunc(node)
					utility = node.reward +0.9*max_val
					if not(node in self.util_list):
						self.util_list[node] = 0
					self.util_list[node] = utility
					if node.typeN == 2:
						self.util_list[node] = 0
			d = 0.0 #reset d
			if abs(utility - self.util_list[node]) > d:
				d = abs(utility - self.util_list[node])		
					#node.u = self.util_list[node]
		print('\n'.join(['	'.join(['{0:.2f}'.format(self.util_list[item]) for item in row]) for row in self.mymap]))

	def MDPfunc(self, n):
		#print "MDP FUNC: ", n
		adj = self.getAdj(n)
		stored_vals = []
		for val in adj:
			if val.x == n.x:
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
						stored_vals.append(0.8*val.reward)
					elif node1 == 0.0:
						stored_vals.append(0.8*val.reward+0.1*(node2.reward))
					elif node2 == 0.0:
						stored_vals.append(0.8*val.reward+0.1*(node1.reward))
					else:
						stored_vals.append(0.8*val.reward+0.1*node1.reward+0.1*node2.reward)
			elif val.y == n.y:
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
						stored_vals.append(0.8*val.reward)
					elif node1 == 0.0:
						stored_vals.append(0.8*val.reward+0.1*node2.reward)
					elif node2 == 0.0:
						stored_vals.append(0.8*val.reward+0.1*node1.reward)
					else:
						stored_vals.append(0.8*val.reward+0.1*node1.reward+0.1*node2.reward)
					
		return max(stored_vals)				
		
		
	#A* search!	
	def starsearch(self):
		locations = 0
		self.Open[self.start] = self.start.reward#self.util_list[self.start]
		while self.Open != {}:
			locations = locations + 1
			#find node.f that is the smallest
			max_val_find = max(self.Open, key=self.Open.get)#we want the largest reward
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
			#print "(", nextNode.x, ",", nextNode.y, ")"
			stringArr.append(["(", nextNode.x, ",", nextNode.y, ")","Utility: ",self.util_list[nextNode]])
			#cost += newCost(nextNode, nextNode.p)
			nextNode = nextNode.p
		stringArr.append(["(", nextNode.x, ",", nextNode.y, ")", "Utility: ",self.util_list[nextNode]])
		for lis in reversed(stringArr):
			print lis[0],lis[1],lis[2],lis[3],lis[4],lis[5],lis[6]
		#print "Total Cost: ", cost
		
		


mymap = getMap(sys.argv[1])
searched = MDP(mymap)
searched.expect_u(float(sys.argv[2]))
searched.starsearch()


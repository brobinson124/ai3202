#Brooke Robinson
#Assignment 7
#Worked with Mario Alanis

#Prior

myArr = [0.82, 0.56, 0.08, 0.81, 0.34, 0.22, 0.37, 0.99, 0.55, 0.61, 0.31, 0.66, 0.28,	1.0, 0.95, 0.71, 0.14, 0.1, 1.0, 0.71,	0.1, 0.6, 0.64, 0.73, 0.39, 0.03, 0.99, 1.0, 0.97, 0.54, 0.8, 0.97,	0.07, 0.69, 0.43, 0.29, 0.61, 0.03, 0.13, 0.14,	0.13, 0.4, 0.94, 0.19, 0.6,	0.68, 0.36, 0.67, 0.12, 0.38, 0.42, 0.81, 0.0, 0.2, 0.85,	0.01, 0.55, 0.3, 0.3, 0.11,	0.83, 0.96,	0.41, 0.65,	0.29, 0.4, 0.54, 0.23, 0.74, 0.65, 0.38, 0.41, 0.82, 0.08, 0.39, 0.97,	0.95, 0.01, 0.62, 0.32,	0.56, 0.68,	0.32, 0.27, 0.77, 0.74,	0.79, 0.11,	0.29, 0.69, 0.99, 0.79,	0.21, 0.2, 0.43, 0.81, 0.9, 0.0, 0.91, 0.01]

def prior():
	
	i = 0
	counter = {"c":0.0,"s|c":0.0,"s|~c":0.0,"r|c":0.0,"r|~c":0.0,"w|sr":0.0,"w|s~r":0.0,"w|~sr":0.0,"w|~s~r":0.0}
	while i < 100:
		#cloudy = False
		#sprinkler = False
		#rain = False
		#wet = False
		#u_c = myArr[i]
		#u_r = myArr[i+1]
		#u_s = myArr[i+2]
		#u_w = myArr[i+3]
		
		#if u_c < 0.5 and u_c >= 0:
		#	cloudy = True
		#if u_r < 0.8 and u_r >= 0:
		#	rain = True
		#if u_s < 0.1 and u_s >= 0:
		#	sprinkler = True
		#if u_w < 0.9 and u_w >= 0:
		#	wet = True
		
		if myArr[i] < 0.5:			#number cloudy is true
			counter["c"] += 1.0
		if myArr[i+1] < 0.1:		#number sprinklers given cloudy
			counter["s|c"] += 1.0
		if myArr[i+1] < 0.5:		#number sprinklers given that cloudy = false
			counter["s|~c"] += 1.0
		if myArr[i+2] < 0.8:		#number of sample where rain is given by cloudy
			counter["r|c"] += 1.0
		if myArr[i+2] < 0.2:		#number of sample where rain is given by cloudy = false
			counter["r|~c"] += 1.0
		if myArr[i+3] < 0.99:		#number of times grass is wet given that sprinkers went off and it rained
			counter["w|sr"] += 1.0
		if myArr[i+3] < 0.9:		#number of times grass is wet given that sprinkers went off and it DIDN'T rain
			counter["w|s~r"] += 1.0
		if myArr[i+3] < 0.9:		#number of times grass is wet given that sprinkers DIDN'T go off and it rained
			counter["w|~sr"] += 1.0
		if myArr[i+3] == 0.0:		#grass is never wet with no rain or sprinklers
			counter["w|~s~r"] += 1.0

		i = i + 4

	#1.a)
	c_true = counter["c"]/25.0
	
	#1.b)
	r = ((counter["r|c"]/25.0)*c_true)+((counter["r|~c"]/25.0)*(1-c_true))
	c_r = ((counter["r|c"]/25.0)*c_true)/r

	#1.c)
	s = ((counter["s|c"]/25.0)*c_true) + ((counter["s|~c"]/25.0)*(1-c_true))
	w_s = ((counter["w|sr"]/25.0)*s*r) + ((counter["w|s~r"]/25.0)*s*(1-r)) + ((counter["w|~s~r"]/25.0)*(1-s)*(1-r))
	
	numerator = (w_s*.5)+(w_s*.5)
	denometor = (w_s) + ((counter["w|~sr"]/25.0)*s*r) + ((counter["w|~s~r"]/25.0)*(1-s)*(1-r))
	
	s_w = numerator/denometor
	
	#1.d)
	numerator = w_s*c_true*(counter["s|c"]/25.0)
	#denometor = ((counter["w|sr"]/25.0)*(counter["s|c"]/25.0)*(counter["r|c"]/25.0) + (counter["w|s~r"]/25.0)*(counter["s|c"]/25.0)*(1-counter
	s_c_w = numerator#/denometor
	
	print "P: P(c=true): ",c_true 
	print "P: P(c=true|rain): ",c_r
	print "P: P(s=true|w) ", s_w
	print "P: P(s=true|c,w) ", s_c_w
	



def rejection():
	prob = {}
	counter = []
	i = 0
	while i < 100:
		c = i
		r = i + 1
		s = i + 2
		w = i + 3

		cloudy = False
		rain = False
		sprinkler = False
		wet = False
		
		if myArr[c] < 0.5:
			cloudy = True
			if myArr[r] < 0.8 and myArr[s] < 0.1: 
				rain = True
				sprinkler = True
				if myArr[w] < 0.99:
					wet = True
					counter.append([cloudy,rain,sprinkler,wet])
				else:
					counter.append([cloudy,rain,sprinkler,wet])
			elif myArr[s] < 0.1 and myArr[r] >= 0.8:
				rain = False
				sprinkler = True
				if myArr[w] < 0.9:
					wet = True
					counter.append([cloudy,rain,sprinkler,wet])
				else:
					counter.append([cloudy,rain,sprinkler,wet])
			elif myArr[r] < 0.8 and myArr[s] >= 0.1:
				rain = True
				sprinkler = False
				if myArr[w] < 0.9:
					wet = True
					counter.append([cloudy,rain,sprinkler,wet])
				else:
					counter.append([cloudy,rain,sprinkler,wet])
			elif myArr[r] >= 0.8 and myArr[s] >= 0.1:
				rain = False
				sprinkler = False
				wet = False #Grass can never be wet when no sprinkler or rain
				counter.append([cloudy,rain,sprinkler,wet])
		if myArr[c] >= 0.5: 
			cloudy = False
			if myArr[r] < 0.2 and myArr[s] < 0.5:
				rain = True
				sprinkler = True
				if myArr[w] < 0.99:
					wet = True
					counter.append([cloudy,rain,sprinkler,wet])
				else:
					counter.append([cloudy,rain,sprinkler,wet])
			elif myArr[r] >= 0.2 and myArr[s] < 0.5:
				rain = False
				sprinkler = True
				if myArr[w] < 0.9:
					wet = True
					counter.append([cloudy,rain,sprinkler,wet])
				else:
					counter.append([cloudy,rain,sprinkler,wet])
			elif myArr[r] < 0.2 and myArr[s] >= 0.5:
				rain = True
				sprinkler = False
				if myArr[w] < 0.9:
					wet = True
					counter.append([cloudy,rain,sprinkler,wet])
				else:
					counter.append([cloudy,rain,sprinkler,wet])
			elif myArr[r] >= 0.2 and myArr[s] >= 0.5:
				rain = False
				sprinkler = False
				wet = False #grass can't be wet
				counter.append([cloudy,rain,sprinkler,wet])
				
		i = i + 4


	#set values in order to call index's easier
	c = 0
	r = 1
	s = 2
	w = 3
	
	
	#3.a)
	x = 0.0
	y = 0.0
	for j in counter:
		if j[c] == True:
			x += 1.0
		if j[c] == False:
			y += 1.0

	print "R: P(c=true): ",x/(x+y)

	#3.b)
	#reset counters
	x = 0.0
	y = 0.0
	for k in counter:
		if k[c] == True and k[r] == True:
			x += 1.0
		if k[c] == False and k[r] == True:
			y += 1.0
			
	print "R: P(c=true|r): ",x/(x+y)

	#3.c)
	#reset again
	x = 0.0
	y = 0.0
	for m in counter:
		if m[s] == True and m[w] == True:
			x += 1.0
		if m[s] == False and m[w] == True:
			y += 1.0
	
	print "R: P(s=true|w): ",x/(x+y)

	#3.d)
	x = 0.0
	y = 0.0
	for n in counter:
		if n[s] == True and n[c] == True and n[w] == True:
			x += 1.0
		if n[s] == False and n[c] == True and n[w] == True:
			y += 1.0
	
	print "R: P(s=true|c,w): ",x/(x+y)

	
	

def exact():
	#P(c=true)
	#P(c=true|rain=true)
	#P(s=true|w=true)
	#P(s=true|c=true,w=true)
	
	prob = {}
	
	prob["c=true"] = 0.5
	prob["c=false"] = 0.5
	
	prob["r=true|c=true"] = 0.8
	prob["r=true|c=false"] = 0.2
	prob["r=false|c=true"] = 0.2
	r_true = prob["r=true|c=true"]*prob["c=true"] + prob["r=true|c=false"]*prob["c=false"]
	prob["r=true"] = r_true
	prob["r=false"] = (1-r_true)
	
	prob["s=true|c=true"] = 0.1
	prob["s=true|c=false"]= 0.5
	prob["s=false|c=true"] = 0.9
	s_true = prob["s=true|c=true"]*prob["c=true"] + prob["s=true|c=false"]*prob["c=false"]
	prob["s=true"] = s_true
	prob["s=false"] = (1-s_true)
	
	prob["w=true|s=true,r=true"] = 0.99
	prob["w=true|s=true,r=false"] = 0.90
	prob["w=true|s=false,r=true"] = 0.90
	prob["w=true|s=false,r=false"] = 0.00
	w_true = (prob["w=true|s=true,r=true"]*prob["s=true"]*prob["r=true"]) + (prob["w=true|s=true,r=false"]*prob["s=true"]*prob["r=false"]) + (prob["w=true|s=false,r=true"]*prob["s=false"]*prob["r=true"]) + (prob["w=true|s=false,r=false"]*prob["s=false"]*prob["r=false"])
	prob["w=true"] = w_true
	
	c_given_r = (prob["r=true|c=true"]*prob["c=true"])/prob["r=true"]
	prob["c=true|r=true"] = c_given_r
	
	w_given_s = (prob["w=true|s=true,r=true"]*prob["s=true"]*prob["r=true"]) + (prob["w=true|s=true,r=false"]*prob["s=true"]*prob["r=false"])
	prob["w=true|s=true"] = w_given_s
	s_given_w = (prob["w=true|s=true"]*prob["s=true"]*prob["r=true"])/prob["w=true"]
	prob["s=true|w=true"] = s_given_w
	
	prob["s"] = .1*.5 + .5*.5
	prob["r"] = .8*.5 + .2*.5
	prob["w|s"] = (.99*prob["s"]*prob["r"]) + (.9*prob["s"]*(1-prob["r"]))
	prob["w"] = (.99*prob["s"]*prob["r"]) + (.9*prob["s"]*(1-prob["r"])) + (.9*(1-prob["s"])*prob["r"]) + .0
	prob["s|w"] = (prob["w|s"]*.5 + prob["w|s"]*.5)/prob["w"]
	
	w_AND_c = prob["w=true|s=true,r=true"]*prob["s=true|c=true"]*prob["r=true|c=true"]*prob["c=true"] + prob["w=true|s=true,r=false"]*prob["s=true|c=true"]*prob["r=false|c=true"]*prob["c=true"] + prob["w=true|s=false,r=true"]*prob["s=false|c=true"]*prob["r=true|c=true"]*prob["c=true"] + prob["w=true|s=false,r=false"]*prob["s=false|c=true"]*prob["r=false|c=true"]*prob["c=true"]
	s_AND_w_AND_c = prob["w=true|s=true"] * prob["s=true|c=true"]*prob["c=true"]
	s_given_w_c = (s_AND_w_AND_c)/(w_AND_c)
	prob["s=true|c=true,w=true"] = s_given_w_c
	
	print "Exact values: "
	print "P(c=true): ", prob["c=true"]
	print "P(c=true|rain=true): ",prob["c=true|r=true"]
	print "P(s=true|w=true): ",prob["s|w"]
	print "P(s=true|c=true,w=true): ",prob["s=true|c=true,w=true"]

print "Prior: "
prior()
exact()
print "Rejection: "
rejection()


#Brooke Robinson
#Assignment 7
#Worked with Mario Alanis

#Prior

myArr = [0.82, 0.56, 0.08, 0.81, 0.34, 0.22, 0.37, 0.99, 0.55, 0.61, 0.31, 0.66, 0.28,	1.0, 0.95, 0.71, 0.14, 0.1, 1.0, 0.71,	0.1, 0.6, 0.64, 0.73, 0.39, 0.03, 0.99, 1.0, 0.97, 0.54, 0.8, 0.97,	0.07, 0.69, 0.43, 0.29, 0.61, 0.03, 0.13, 0.14,	0.13, 0.4, 0.94, 0.19, 0.6,	0.68, 0.36, 0.67, 0.12, 0.38, 0.42, 0.81, 0.0, 0.2, 0.85,	0.01, 0.55, 0.3, 0.3, 0.11,	0.83, 0.96,	0.41, 0.65,	0.29, 0.4, 0.54, 0.23, 0.74, 0.65, 0.38, 0.41, 0.82, 0.08, 0.39, 0.97,	0.95, 0.01, 0.62, 0.32,	0.56, 0.68,	0.32, 0.27, 0.77, 0.74,	0.79, 0.11,	0.29, 0.69, 0.99, 0.79,	0.21, 0.2, 0.43, 0.81, 0.9, 0.0, 0.91, 0.01]

def prior():
	counter = 0
	i = 0
	cloudy = False
	sprinkler = False
	rain = False
	wet = False
	sample = []
	while i < 100:
		cloudy = False
		sprinkler = False
		rain = False
		wet = False
		u_c = myArr[i]
		u_r = myArr[i+1]
		u_s = myArr[i+2]
		u_w = myArr[i+3]
		
		if u_c < 0.5 and u_c >= 0:
			cloudy = True
		if u_r < 0.8 and u_r >= 0:
			rain = True
		if u_s < 0.1 and u_s >= 0:
			sprinkler = True
		if u_w < 0.9 and u_w >= 0:
			wet = True
		
		
		
		sample.append([cloudy, rain, sprinkler, wet])
		
		counter = counter +1
		i = i + 4
	
	num_c_true = 0.0
	num_c_given_rain = 0.0
	num_s_given_w = 0.0
	num_s_given_c_w = 0.0
	for val in sample:
		if val[0] == True:
			num_c_true = num_c_true + 1.0
		if val[0] == True and val[1] == True:
			num_c_given_rain = num_c_given_rain + 1.0
		if val[2] == True and val[3] == True:
			num_s_given_w = num_s_given_w + 1.0
		if val[2] == True and val[3] == True and val[0] == True:
			num_s_given_c_w = num_s_given_c_w + 1.0
			
	print (num_c_true)
	c_true = num_c_true/25
	c_given_rain = num_c_given_rain/25
	s_given_w = num_s_given_w/25
	s_given_c_w = num_s_given_c_w/25
	print "P: P(c=true): ",c_true 
	print "P: P(c=true|rain): ",c_given_rain
	print "P: P(s=true|w ", s_given_w 
	print "P: P(s=true|c,w ", s_given_c_w 
	


def rejection(keepers):
	counter = 0.0
	i = 0
	cloudy = False
	sprinkler = False
	rain = False
	wet = False
	sample = []
	while i < 100:
		cloudy = False
		sprinkler = False
		rain = False
		wet = False
		u_c = myArr[i]
		u_r = myArr[i+1]
		u_s = myArr[i+2]
		u_w = myArr[i+3]
		
		if u_c < 0.5 and u_c >= 0:
			cloudy = True
		if u_r < 0.8 and u_r >= 0:
			rain = True
		if u_s < 0.1 and u_s >= 0:
			sprinkler = True
		if u_w < 0.9 and u_w >= 0:
			wet = True
		
		
		if keepers == "c":
			if cloudy == True:
				sample.append([cloudy, rain, sprinkler, wet])
				counter = counter +1.0
		elif keepers == "c_given_r":
			if cloudy == True and rain == True:
				sample.append([cloudy, rain, sprinkler, wet])
				counter = counter +1.0
		elif keepers == "s_given_w":
			if sprinkler == True and wet == True:
				sample.append([cloudy, rain, sprinkler, wet])
				counter = counter +1.0
		elif keepers == "s_given_c_w":
			if sprinkler == True and wet == True and cloudy == True:
				sample.append([cloudy, rain, sprinkler, wet])
				counter = counter +1.0
				
				
		i = i + 4
		
		
		
	if keepers == "c":
		print "R: P(c=true): ", (counter/25.0)
	elif keepers == "c_given_r":
		print"R: P(c=true|rain): ", (counter/25.0)
	elif keepers == "s_given_w":
		print "R: P(s=true|w) ", (counter/25.0)
	elif keepers == "s_given_c_w":
		print "P(s=true|c,w) ", (counter/25.0)
		

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
	r_true = prob["r=true|c=true"]*prob["c=true"] + prob["r=true|c=false"]*prob["c=false"]
	prob["r=true"] = r_true
	prob["r=false"] = (1-r_true)
	
	prob["s=true|c=true"] = 0.1
	prob["s=true|c=false"]= 0.5
	s_true = prob["s=true|c=true"]*prob["c=true"] + prob["s=true|c=false"]*prob["c=false"]
	prob["s=true"] = s_true
	prob["s=false"] = (1-s_true)
	
	prob["w=true|s=true,r=true"] = 0.99
	prob["w=true|s=true,r=false"] = 0.90
	prob["w=true|s=false,r=true"] = 0.90
	prob["w=true|s=false,r=false"] = 0.00
	w_true = prob["w=true|s=true,r=true"]*prob["s=true"]*prob["r=true"] + prob["w=true|s=true,r=false"]*prob["s=true"]*prob["r=false"] + prob["w=true|s=false,r=true"]*prob["s=false"]*prob["r=true"] + prob["w=true|s=false,r=false"]*prob["s=false"]*prob["r=false"]
	prob["w=true"] = w_true
	
	c_given_r = (prob["r=true|c=true"]*prob["c=true"])/prob["r=true"]
	prob["c=true|r=true"] = c_given_r
	
	w_given_s =  prob["w=true|s=true,r=true"]*prob["s=true"]*prob["r=true"] + prob["w=true|s=true,r=false"]*prob["s=true"]*prob["r=false"]
	prob["w=true|s=true"] = w_given_s
	s_given_w = (prob["w=true|s=true"]*prob["s=true"])/prob["w=true"]
	prob["s=true|w=true"] = s_given_w
	
	w_AND_c = prob["w=true"] * prob["c=true"]
	s_AND_w_AND_c = prob["w=true|s=true"] * prob["s=true|c=true"]*prob["c=true"]
	s_given_w_c = (s_AND_w_AND_c)/(w_AND_c)
	prob["s=true|c=true,w=true"] = s_given_w_c
	
	print "Exact values: "
	#P(c=true)
	print prob["c=true"]
	#P(c=true|rain=true)
	print prob["c=true|r=true"]
	#P(s=true|w=true)
	print prob["s=true|w=true"]
	#P(s=true|c=true,w=true)
	print prob["s=true|c=true,w=true"]

prior()
rejection("c")
rejection("c_given_r")
rejection("s_given_w")
rejection("s_given_c_w")
exact()

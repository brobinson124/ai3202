#Assignment 6
#Bays Nets

import getopt
import sys

prob_dict= {}

class Node:
	
	def __init__(self, name):
		self.name = name
		self.conditionals = {}
		self.prob = {}

	def set_prob(self, key, value):
		self.prob[key] = value
		
	def __str__(self):
		return (str(self.name))

def setNodes(pollution_val, smoker_val):
	#NOTE: "high pollution" = ~P
	#..... "low pollution" = P
	
	nodes = []
	
	#Smoker
	smoker = Node("Smoker")
	smoker.set_prob("T", smoker_val)
	smoker.set_prob("F", (1-smoker_val))
	
	#Pollution
	pollution = Node("Pollution")
	pollution.set_prob("L", pollution_val)
	pollution.set_prob("H", (1-pollution_val))
	
	#Cancer
	cancer = Node("Cancer")
	cancer.set_prob("~PS", .05) #high p, s
	cancer.set_prob("~P~S", .02) #high p, non-s
	cancer.set_prob("PS", .03) #low p, s
	cancer.set_prob("P~S", .001) #low p, non-s

	#Xray
	x = Node("XRay")
	x.set_prob("C", .9) #c=T
	x.set_prob("~C",.2) #c=F
	
	#Dyspnoea aka breathing problems
	d = Node("Dyspnoea")
	d.set_prob("C", .65) #c = T
	d.set_prob("~C", .3) #c = F

	nodes.append(smoker)
	nodes.append(pollution)
	nodes.append(cancer)
	nodes.append(x)
	nodes.append(d)
	
	return nodes

'''
Marginals
'''

def marginal_c(cancer, pollution, smoker):
	first = cancer.prob["~PS"] * (1.0 - pollution.prob["L"]) * smoker.prob["T"]
	second = cancer.prob["~P~S"] * (1.0 - pollution.prob["L"]) * (1.0 - smoker.prob["T"])
	third= cancer.prob["PS"] * pollution.prob["L"] * smoker.prob["T"]
	fourth = cancer.prob["P~S"] * pollution.prob["L"] * (1.0 - smoker.prob["T"])
	 
	prob = first + second + third + fourth
	
	prob_dict["marg_c"] = prob
	prob_dict["~marg_c"] = 1-prob
	
	return prob

def marginal_d(cancer, d):	
	first = d.prob["C"] * prob_dict["marg_c"]
	second = d.prob["~C"] * prob_dict["~marg_c"]
	
	prob = first + second
	
	prob_dict["d"] = prob
	prob_dict["~d"] = 1-prob
	return prob
	
def marginal_x(cancer, x):
	first = x.prob["C"] * prob_dict["marg_c"]
	second = x.prob["~C"] * prob_dict["~marg_c"]
	
	prob = first + second
	
	prob_dict["x"] = prob
	prob_dict["~x"] = 1-prob
	return prob
	
'''
Conditionals
'''
def c_given_s(cancer, pollution, smoker):
	prob = cancer.prob["PS"] * pollution.prob["L"] * smoker.prob["T"] + (cancer.prob["~PS"] * pollution.prob["H"] * smoker.prob["T"])
	prob = prob / smoker.prob["T"]
	prob_dict["c_given_s"] = prob
	
	return prob	
	
def s_given_c(cancer, pollution, smoker):	
	
	c_given_s(cancer, pollution, smoker)
	
	prob = (prob_dict["c_given_s"] * smoker.prob["T"])/prob_dict["marg_c"]
	prob_dict["s_given_c"] = prob
	
	return prob
	
def x_given_s(cancer, x, pollution, smoker):
	#numerator = joint_XSCP(cancer,x, pollution, smoker)
	#denometor = joint_SCP(cancer, pollution, smoker)
	
	prob_1 = x.prob["C"] * (cancer.prob["PS"]*smoker.prob["T"]*pollution.prob["L"])
	prob_2 = x.prob["C"] * (cancer.prob["~PS"]*smoker.prob["T"]*pollution.prob["H"])
	prob_3 = x.prob["~C"] * ((1- cancer.prob["PS"])*smoker.prob["T"]*pollution.prob["L"])
	prob_4 = x.prob["~C"] * ((1- cancer.prob["~PS"])*smoker.prob["T"]*pollution.prob["H"])
	denometor_1 = cancer.prob["PS"]*pollution.prob["L"]*smoker.prob["T"]
	denometor_2 = cancer.prob["~PS"]*pollution.prob["H"]*smoker.prob["T"]
	denometor_3 = (1-cancer.prob["PS"])*pollution.prob["L"]*smoker.prob["T"]
	denometor_4 = (1-cancer.prob["~PS"])*pollution.prob["H"]*smoker.prob["T"]
	
	numerator = prob_1+prob_2+prob_3+prob_4
	denometor = denometor_1+denometor_2+denometor_3+denometor_4
	
	prob = numerator/denometor
	
	prob_dict["x_given_s"] = prob
	
	return prob
	
def x_given_d(x, d, cancer, pollution, smoker):
	#prob(x|c)*P(c)*P(d|c) + P(x|~c)*P(~c)*P(d|~c)  /  P(d)
	marginal_c(cancer, pollution, smoker)
	marginal_d(cancer,d)
	val = ((x.prob["C"]*prob_dict["marg_c"]*d.prob["C"]) + (x.prob["~C"]*prob_dict["~marg_c"]*d.prob["~C"])) / prob_dict["d"]
	
	prob_dict["x_given_d"] = val
	
	return val
	
def c_given_d_s(d, smoker, cancer, pollution):
	#P(c,d,s) / P(d,s)   p is hidden
	numerator_first = d.prob["C"] * cancer.prob["PS"] * pollution.prob["L"] * smoker.prob["T"]
	numerator_second = d.prob["C"] * cancer.prob["~PS"] * pollution.prob["H"] * smoker.prob["T"]
	numerator = numerator_first + numerator_second
	denometor_first = d.prob["C"] * cancer.prob["PS"] * pollution.prob["L"] * smoker.prob["T"]
	denometor_second = d.prob["C"] * cancer.prob["~PS"] * pollution.prob["H"] * smoker.prob["T"]
	denometor_third = d.prob["~C"] * (1-cancer.prob["PS"]) * pollution.prob["L"] * smoker.prob["T"]
	denometor_fourth = d.prob["~C"] * (1-cancer.prob["~PS"]) * pollution.prob["H"] * smoker.prob["T"]
	denometor = denometor_first + denometor_second + denometor_third + denometor_fourth
	
	val = numerator/denometor
	
	prob_dict["c_given_d_s"] = val
	
	return prob_dict["c_given_d_s"]

def d_given_p_high(d, pollution, smoker, cancer):
	prob_1 = d.prob["C"] * (cancer.prob["~PS"]*smoker.prob["T"]*pollution.prob["H"])
	prob_2 = d.prob["C"] * (cancer.prob["~P~S"]*smoker.prob["F"]*pollution.prob["H"])
	prob_3 = d.prob["~C"] * ((1-cancer.prob["~PS"])*smoker.prob["T"]*pollution.prob["H"])
	prob_4 = d.prob["~C"] * ((1-cancer.prob["~P~S"])*smoker.prob["F"]*pollution.prob["H"])
	denometor_1 = cancer.prob["~PS"]*pollution.prob["H"]*smoker.prob["T"]
	denometor_2 = cancer.prob["~P~S"]*pollution.prob["H"]*smoker.prob["F"]
	denometor_3 = (1-cancer.prob["~PS"])*pollution.prob["H"]*smoker.prob["T"]
	denometor_4 = (1-cancer.prob["~P~S"])*pollution.prob["H"]*smoker.prob["F"]
	
	numerator = prob_1+prob_2+prob_3+prob_4
	denometor = denometor_1+denometor_2+denometor_3+denometor_4
	
	val = numerator/denometor
	
	prob_dict["d_given_p_high"] = val
	
	return prob_dict["d_given_p_high"]
	
def p_high_given_d(d,pollution,smoker,cancer):
	prob = (d_given_p_high(d, pollution, smoker, cancer) * pollution.prob["H"] ) /prob_dict["d"]
	
	prob_dict["p_high_given_d"] = prob
	
	return prob_dict["p_high_given_d"]

	
def d_given_s(d, pollution, smoker, cancer, x):
	prob_1 = d.prob["C"] * (cancer.prob["PS"]*smoker.prob["T"]*pollution.prob["L"])
	prob_2 = d.prob["C"] * (cancer.prob["~PS"]*smoker.prob["T"]*pollution.prob["H"])
	prob_3 = d.prob["~C"] * ((1- cancer.prob["PS"])*smoker.prob["T"]*pollution.prob["L"])
	prob_4 = d.prob["~C"] * ((1- cancer.prob["~PS"])*smoker.prob["T"]*pollution.prob["H"])
	denometor_1 = cancer.prob["PS"]*pollution.prob["L"]*smoker.prob["T"]
	denometor_2 = cancer.prob["~PS"]*pollution.prob["H"]*smoker.prob["T"]
	denometor_3 = (1-cancer.prob["PS"])*pollution.prob["L"]*smoker.prob["T"]
	denometor_4 = (1-cancer.prob["~PS"])*pollution.prob["H"]*smoker.prob["T"]
	
	numerator = prob_1+prob_2+prob_3+prob_4
	denometor = denometor_1+denometor_2+denometor_3+denometor_4
	
	top = joint_d_s_c_p(pollution, cancer, smoker, d, x)
	bottom = joint_s_c_p(pollution, cancer, smoker, d, x)
	
	val = numerator/denometor
	#val = top/bottom
	prob_dict["d_given_s"] = val
	
	return prob_dict["d_given_s"]
	
def s_given_d(d,pollution,smoker,cancer, x):
	prob = (d_given_s(d, pollution, smoker, cancer,x) * smoker.prob["T"]) / prob_dict["d"]
	prob_dict["s_given_d"] = prob
	
	return prob_dict["s_given_d"]
	
def c_given_d(cancer, d):
	prob = ( d.prob["C"] * prob_dict["marg_c"] ) / prob_dict["d"]
	
	prob_dict["c_given_d"] = prob
	
	return prob

def c_given_p_high(cancer, x, pollution, smoker):
	first = cancer.prob["~PS"] * pollution.prob["H"] * smoker.prob["T"]
	second = cancer.prob["~P~S"] * pollution.prob["H"] * smoker.prob["F"]
	
	prob = (first+second)/pollution.prob["H"]
	
	prob_dict["c_given_p_high"] = prob
	
	return prob
	
def c_given_p_low(cancer, x, pollution, smoker):
	first = cancer.prob["PS"] * pollution.prob["L"] * smoker.prob["T"]
	second = cancer.prob["P~S"] * pollution.prob["L"] * smoker.prob["F"]
	
	prob = (first+second)/pollution.prob["L"]
	
	prob_dict["c_given_p_low"] = prob
	
	return prob
	
def p_high_given_c(cancer, x, pollution, smoker):
	c_given_p_high(cancer, x, pollution, smoker)
	numerator = prob_dict["c_given_p_high"] * pollution.prob["H"]
	denometor = prob_dict["marg_c"]
	
	prob = numerator/denometor
	
	prob_dict["p_high_given_c"] = prob
	
	return prob
	
def d_given_c(pollution, cancer, smoker, d):
	c_given_d(cancer, d)
	marginal_d(cancer, d)
	marginal_c(cancer, pollution, smoker)
	numerator = prob_dict["c_given_d"] * prob_dict["d"]
	denometor = prob_dict["marg_c"]
	
	prob = numerator/denometor
	
	prob_dict["d_given_c"] = prob
	
	return prob
	
########
#TESTER#
##########################################

def s_given_c_p(pollution, cancer, smoker, d, x):
	numerator = smoker.prob["T"] * cancer.prob["PS"] * pollution.prob["L"]
	denomater = cancer.prob["PS"] * pollution.prob["L"] * smoker.prob["T"] + cancer.prob["P~S"] * pollution.prob["L"] * smoker.prob["F"]
	
	prob = numerator/denomater
	
	prob_dict["s_given_c_p"] = prob
	
	return prob
	
def joint_s_c_p(pollution, cancer, smoker, d, x):
	s_given_c_p(pollution, cancer, smoker, d, x)
	c_given_p_low(cancer, x, pollution, smoker)
	prob = prob_dict["s_given_c_p"] * prob_dict["c_given_p_low"] * pollution.prob["L"]
	
	prob_dict["joint_s_c_p"] = prob
	
	return prob
	
def joint_d_s_c_p(pollution, cancer, smoker, d, x):
	s_given_c_p(pollution, cancer, smoker, d, x)
	joint_s_c_p(pollution, cancer, smoker, d, x)
	d_given_c(pollution, cancer, smoker, d)
	s_given_c_p(pollution, cancer, smoker, d, x)
	
	numerator = prob_dict["d_given_c"]*cancer.prob["PS"]*smoker.prob["T"]*pollution.prob["L"]*prob_dict["s_given_c_p"]*pollution.prob["L"]
	denometor = prob_dict["joint_s_c_p"]
	
	prob = numerator/denometor
	
	prob_dict["joint_d_s_c_p"] = prob
	
	return prob

#####################################	
	
def p_high_given_c_s(smoker, cancer, pollution, x):
	p_high_given_c(cancer, x, pollution, smoker)
	numerator = cancer.prob["~PS"] * smoker.prob["T"] * pollution.prob["H"]
	denometor = cancer.prob["~PS"]*smoker.prob["T"]*pollution.prob["H"] + cancer.prob["PS"]*smoker.prob["T"]*pollution.prob["L"]
	
	p = numerator/denometor
	
	prob_dict["p_high_given_c_s"] = p
	
	return p
	
	
def p_high_given_d_s(smoker, cancer, pollution, d):
	n1 = d.prob["C"]*cancer.prob["~PS"]*pollution.prob["H"]*smoker.prob["T"]
	n2 = d.prob["~C"]*(1-cancer.prob["~PS"])*pollution.prob["H"]*smoker.prob["T"]
	d1 = d.prob["C"]*cancer.prob["~PS"]*pollution.prob["H"]*smoker.prob["T"]
	d2 = d.prob["C"]*cancer.prob["PS"]*pollution.prob["L"]*smoker.prob["T"]
	d3 = d.prob["~C"]*(1-cancer.prob["~PS"])*pollution.prob["H"]*smoker.prob["T"]
	d4 = d.prob["~C"]*(1-cancer.prob["PS"])*pollution.prob["L"]*smoker.prob["T"]
	
	numerator = n1+n2
	denomater = d1+d2+d3+d4
	
	p = numerator/denomater
	
	prob_dict["p_high_given_d_s"] = p
	
	return p
	
def x_given_d_s(smoker, cancer, pollution, d, x):
	n1 = x.prob["C"]*d.prob["C"]*cancer.prob["~PS"]*pollution.prob["H"]*smoker.prob["T"]
	n2 = x.prob["~C"]*d.prob["~C"]*(1-cancer.prob["~PS"])*pollution.prob["H"]*smoker.prob["T"]	
	n3 = x.prob["C"]*d.prob["C"]*cancer.prob["PS"]*pollution.prob["L"]*smoker.prob["T"]
	n4 = x.prob["~C"]*d.prob["~C"]*(1-cancer.prob["PS"])*pollution.prob["L"]*smoker.prob["T"]
	d1 = d.prob["C"]*cancer.prob["~PS"]*pollution.prob["H"]*smoker.prob["T"]
	d2 = d.prob["~C"]*(1-cancer.prob["~PS"])*pollution.prob["H"]*smoker.prob["T"]	
	d3 = d.prob["C"]*cancer.prob["PS"]*pollution.prob["L"]*smoker.prob["T"]
	d4 = d.prob["~C"]*(1-cancer.prob["PS"])*pollution.prob["L"]*smoker.prob["T"]

	num = n1+n2+n3+n4
	den = d1+d2+d3+d4
	
	p = num/den
	
	prob_dict["x_given_d_s"] = p
	
	return p

def main():
	print "conditional probability arguments need to be in double quotes."
	try:
		opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
	except getopt.GetoptError as err:
		print str(err)
		sys.exit(2)
	output = None
	p_output = None
	val = None
	operation = None
	for o, a in opts:
		if o in ("-j"):
			operation = o
			output = a
		elif o in ("-m"):
			operation = o
			output = a
		elif o in ("-g"):
			operation = o
			output = a
		elif o in ("-p"):
			p_output = a[0]
			val = float(a[1:])
			output = a[0]
		else: 
			assert False, "unhandled option"

	print output#now store the output into a node
    
	pollution_val = .9
	smoker_val = .3
	
	
	nodes = []
	
	if (p_output == "S"):
		smoker_val = val
		nodes = setNodes(pollution_val, smoker_val)
	elif (p_output == "P"):
		pollution_val = val
		nodes = setNodes(pollution_val, smoker_val)
	else:
		nodes = setNodes(pollution_val, smoker_val)
		
	smoker = nodes[0]
	pollution = nodes[1]
	cancer = nodes[2]
	x = nodes[3]
	d = nodes[4]
		
#call functions to do math
	marg_c = marginal_c(cancer,pollution, smoker)
	marg_d = marginal_d(cancer, d)
	marg_x = marginal_x(cancer, x)
	
	if operation == "-m":
		if output == "c":
			print(marg_c)
		elif output == "~c":
			print(prob_dict["~marg_c"])
		elif output == "s":
			print(smoker_val)
		elif output == "~s":
			opposite_val = 1- smoker_val 
			print(opposite_val)
		elif output == "p":
			print(pollution_val)
		elif output == "~p":
			opposite_val_p = 1 - pollution_val
			print(opposite_val_p)
		elif output == "x":
			print "Not written yet"
		elif output == "~x":
			print "Not written yet"
		elif output == "d":
			print(marg_d)
		elif output == "~d":
			print prob_dict["~d"]
		else:
			print("Not a valid option")
			sys.exit(2)
			
	if operation == "-g":
		if output == "p|p" or output == "~p|~p":
			print "1"
		if output == "p|s":
			print(pollution_val)
		if output == "p|c":
			print p_given_c(cancer, x, pollution, smoker)
		if output == "~p|d":
			print p_high_given_d(d, pollution, smoker, cancer)
		if output == "~p|s":
			print(1 - pollution_val)
		if output == "~p|c":
			print p_high_given_c(cancer, x, pollution, smoker)
		if output == "~p|sc" or output == "~p|cs":
			print p_high_given_c_s(smoker, cancer, pollution, x)
		if output == "~p|ds" or output == "~p|sd":
			print p_high_given_d_s(smoker, cancer, pollution, d)
			
		if output == "s|s" or output == "s|sd" or output == "s|ds" or output == "s|cs" or output == "s|sc":
			print "1"
		if output == "s|p":
			print(smoker_val)
		if output == "s|c":
			print s_given_c(cancer, pollution, smoker)
		if output == "s|d":
			print s_given_d(d, pollution, smoker, cancer, x)
			
		if output == "d|d" or output == "d|ds" or output == "d|sd":
			print "1"
		if output == "d|s":
			print d_given_s(d, pollution, smoker, cancer, x)
		if output == "d|p":
			print (1 - d_given_p_high(d, pollution, smoker, cancer))
		if output == "d|~p":
			print d_given_p_high(d, pollution, smoker, cancer)
		if output == "d|c" or output == "d|cs" or output == "d|sc":
			print d_given_c(pollution, cancer, smoker, d)
			
		if output == "c|c" or output == "c|cs" or output == "c|sc":
			print "1"
		if output == "c|d":
			print c_given_d(cancer, d)
		if output == "c|s":
			print c_given_s(cancer, pollution, smoker)
		if output == "c|ds" or output == "c|sd":
			print c_given_d_s(d, smoker, cancer, pollution)
			
		if output == "x|x":
			print "1"
		if output == "x|s":
			print x_given_s(cancer, x, pollution, smoker)
		if output == "x|d":
			print x_given_d(x,d, cancer, pollution, smoker)
		if output == "x|c" or output == "x|cs" or output == "x|sc":
			print x.prob["C"]
		if output == "x|ds" or output == "x|sd":
			print x_given_d_s(smoker, cancer, pollution, d, x)


if __name__ == "__main__":
    main()

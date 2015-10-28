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
	numerator = joint_XSCP(cancer,x, pollution, smoker)
	denometor = joint_SCP(cancer, pollution, smoker)
	
	prob = numerator/denometor
	
	prob_dict["x_given_s"] = prob
	
	return prob
	
def x_given_d(x, d):
	#prob(x|c)*P(c)*P(d|c) + P(x|~c)*P(~c)*P(d|~c)  /  P(d)
	val = ((x.prob["C"]*prob_dict["C"]*d.prob["C"]) + (x.prob["~C"]*prob_dict["~C"]*d.prob["~C"])) / prob_dict["d"]
	
	prob_dict["x_given_d"] = val
	
	return prob_dict
	
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
#########
##WRONG##
#########
def d_given_p_high(d, pollution, smoker, cancer):
	prob_1 = d.prob["C"] * (cancer.prob["~PS"]*smoker.prob["T"]*pollution.prob["H"])
	prob_2 = d.prob["C"] * (cancer.prob["~P~S"]*smoker.prob["F"]*pollution.prob["H"])
	prob_3 = d.prob["~C"] * (cancer.prob["~PS"]*smoker.prob["T"]*pollution.prob["H"])
	prob_4 = d.prob["~C"] * (cancer.prob["~P~S"]*smoker.prob["F"]*pollution.prob["H"])
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
	prob = (d_given_p_high(d, pollution, smoker, cancer) * prob_dict["d"]) / pollution.prob["H"]
	
	prob_dict["p_high_given_d"] = prob
	
	return prob_dict["p_high_given_d"]

	
def d_given_s(d, pollution, smoker, cancer):
	prob_1 = d.prob["C"] * (cancer.prob["PS"]*smoker.prob["T"]*pollution.prob["L"])
	prob_2 = d.prob["C"] * (cancer.prob["~PS"]*smoker.prob["T"]*pollution.prob["H"])
	prob_3 = d.prob["~C"] * (cancer.prob["PS"]*smoker.prob["T"]*pollution.prob["L"])
	prob_4 = d.prob["~C"] * (cancer.prob["~PS"]*smoker.prob["T"]*pollution.prob["H"])
	denometor_1 = cancer.prob["PS"]*pollution.prob["L"]*smoker.prob["T"]
	denometor_2 = cancer.prob["~PS"]*pollution.prob["H"]*smoker.prob["T"]
	denometor_3 = (1-cancer.prob["PS"])*pollution.prob["L"]*smoker.prob["T"]
	denometor_4 = (1-cancer.prob["~PS"])*pollution.prob["H"]*smoker.prob["T"]
	
	numerator = prob_1+prob_2+prob_3+prob_4
	denometor = denometor_1+denometor_2+denometor_3+denometor_4
	
	val = numerator/denometor
	
	prob_dict["d_given_s"] = val
	
	return prob_dict["d_given_s"]
	
def s_given_d(d,pollution,smoker,cancer):
	prob = (d_given_s(d, pollution, smoker, cancer) * prob_dict["d"]) / smoker.prob["T"]
	
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
		if output == "p|p":
			print(pollution_val)
		if output == "p|s":
			print(pollution_val)
		if output == "p|c":
			print p_given_c(cancer, x, pollution, smoker)
		if output == "~p|d":
			print p_high_given_d(d, pollution, smoker, cancer)
		if output == "~p|s":
			print(pollution_val)
		if output == "~p|c":
			print p_high_given_c(cancer, x, pollution, smoker)
			
		if output == "s|s":
			print(smoker_val)
		if output == "s|p":
			print(smoker_val)
		if output == "s|c":
			print s_given_c(cancer, pollution, smoker)
		if output == "s|d":
			print s_given_d(d, pollution, smoker, cancer)
			
		if output == "d|d":
			print prob_dict["d"]
		if output == "d|s":
			print d_given_s(d, pollution, smoker, cancer)
		if output == "d|p":
			print (1 - d_given_p_high(d, pollution, smoker, cancer))
		if output == "d|~p":
			print d_given_p_high(d, pollution, smoker, cancer)
		if output == "d|c":
			print d_given_c(pollution, cancer, smoker, d)
			
		if output == "c|c":
			print marginal_c(cancer, pollution, smoker)
		if output == "c|d":
			print c_given_d(cancer, d)
		if output == "c|s":
			print c_given_s(cancer, pollution, smoker)
		
			
	print "Next step: Joints"
	
	print "How to do distributions???"


if __name__ == "__main__":
    main()

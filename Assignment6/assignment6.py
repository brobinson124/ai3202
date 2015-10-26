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


	
	prob_dict["C"] = val_c
	prob_dict["~C"] = 1-val_c
	
def marginal_c(c, p, s):
	
	
def conditional(node):
	
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
	
def d_given_p_high(d, pollution, smoker, cancer):
	prob_1 = d.prob["C"] * (cancer.prob["~PS"]*smoker.prob["T"]*pollution["H"])
	prob_2 = d.prob["C"] * (cancer.prob["~P~S"]*smoker.prob["F"]*pollution["H"])
	prob_3 = d.prob["~C"] * (cancer.prob["~PS"]*smoker.prob["T"]*pollution["H"])
	prob_4 = d.prob["~C"] * (cancer.prob["~P~S"]*smoker.prob["F"]*pollution["H"])
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
	prob_1 = d.prob["C"] * (cancer.prob["PS"]*smoker.prob["T"]*pollution["L"])
	prob_2 = d.prob["C"] * (cancer.prob["~PS"]*smoker.prob["T"]*pollution["H"])
	prob_3 = d.prob["~C"] * (cancer.prob["PS"]*smoker.prob["T"]*pollution["L"])
	prob_4 = d.prob["~C"] * (cancer.prob["~PS"]*smoker.prob["T"]*pollution["H"])
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
	prob = ( d.prob["C"] * prob_dict["marge_c"] ) / prob_dict["d"]
	
	prob_dict["c_given_d"] = prob_dict
	
	return prob

	
	
def main():
    try:
		opts, args = getopt.getopt(sys.argv[1:], "m:vg:aj:bp:c", ["marginal=", "conditional=","joint=","prior"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
       # usage()
        sys.exit(2)
    output = None
    p_output = None
    val = None
    for o, a in opts:
        if o in ("-j"):
			output = a
        elif o in ("-m"):
            output = a
        elif o in ("-g"):
            output = a
        elif o in ("-p"):
			p_output = a[0]
			val = float(a[1:])
        else:
            assert False, "unhandled option"
    # ...
    print output#now store the output into a node
    
    pollution_val = .1
    smoker_val = .3
    
    if p_output = "s":
		setNodes(pollution_val, val)
	elif p_output = "p":
		setNodes(val, smoker_val)
	else:
		setNodes(pollution_val, smoker_val)
		

	#call functions to do math
    


if __name__ == "__main__":
    main()

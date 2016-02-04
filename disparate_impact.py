#feature_to_repair, response are both lists, groups and outcomes are tuples
#Pr(C=1|X=0)/Pr(C=1|X=1)
def disparate_impact(feature_to_repair, response, groups, outcomes):
	#assert len(feature_to_repair) == len(response), and groups and outcomes are tuples
	total = len(feature_to_repair)
	group_x = [0]*total
	group_y = [0]*total
	group_x_and_a = [0]*total	
	group_y_and_a = [0]*total	
	for i, group in enumerate(feature_to_repair):
		if group == groups[0]:
			group_x[i] = 1
		elif group == groups[1]:
			group_y[i] = 1 
	for i,dummy in enumerate(group_x):
		if (dummy==1) and (response[i] == outcomes[0]):
			group_x_and_a[i]=1
	for i,dummy in enumerate(group_y):
		if (dummy==1) and (response[i] == outcomes[0]):
			group_y_and_a[i]=1	
	prob_x = sum(group_x) / float(total)
	prob_y = sum(group_y) / float(total)
	prob_x_and_a = sum(group_x_and_a) / float(total)
	prob_y_and_a = sum(group_y_and_a) / float(total)
	prob_a_given_x = prob_x_and_a / prob_x
	prob_a_given_y = prob_y_and_a / prob_y
	return prob_a_given_y/prob_a_given_x

def test():
	feature_to_repair = ['W','W','B','B','W']
	response = [0,1,1,0,1]
	groups = ('W','B')
	outcomes = (1,0)
	di = disparate_impact(feature_to_repair, response, groups, outcomes)
	print "Disparate Impact correct?", di==0.75 

if __name__== "__main__":
  test()

import networkx as nx
from collections import defaultdict
import random

class CategoricalFeature:
  def __init__(self, data, name="no_name"):
    self.data = data
    self.name = name
    d1=defaultdict(int) #bin_data
    d2=defaultdict(int) #bin_index_dict
    d3=defaultdict(list) #bin_fulldata
    d4=defaultdict(int) #bin_index_dict_reverse
    d5=defaultdict(int) #category_count

    n = len(self.data)
    count = 0
    for i in range(0,n):
      obs = self.data[i]
      if obs in d2: pass  # if obs (i.e. category) is alreay a KEY in bin_index_data then don't do anything
      else:
        d2[obs] = count #bin_index_dict inits the KEY: category, with VALUE: count
        d4[count] = obs #bin_index_dict_reverse does the opposite
        count += 1
      bin_idx = d2[obs]
      d1[bin_idx] += 1 #add 1 to the obs category idex in bin_data
      d5[obs] += 1 #add 1 to the obs category NAME in category_count
      d3[bin_idx].append(i) #add obs to the list of obs with that category in bin_fulldata

    self.bin_data = d1
    self.category_count = d5
    self.num_bins = len(d1.items())
    self.bin_fulldata = d3
    self.bin_index_dict = d2
    self.bin_index_dict_reverse = d4


  def create_graph(self): #creates graph given a CategoricalFeature object
    DG=nx.DiGraph() #using networkx package
    bin_list = self.bin_data.items()
    bin_index_dict_reverse = self.bin_index_dict_reverse
    desired_category_count = self.desired_category_count
    k = self.num_bins
    DG.add_node('s')
    DG.add_node('t')
    for i in range(0, k): #lefthand side nodes have capacity = number of observations in category i
      DG.add_node(i)
      DG.add_edge('s', i, {'capacity' : bin_list[i][1], 'weight' : 0})
    for i in range(k, 2*k): #righthand side nodes have capacity = DESIRED number of observations in category i
      DG.add_node(i)
      cat = bin_index_dict_reverse[i-k]
      DG.add_edge(i, 't', {'capacity' : desired_category_count[cat], 'weight' : 0})
    #Add special node to hold overflow
    DG.add_node(2*k)
    DG.add_edge(2*k, 't', {'weight' : 0})
    for i in range(0, k):
      for j in range(k,2*k): #for each edge from a lefthand side node to a righhand side node:
        if (i+k)==j:  #IF they represent the same category, the edge weight is 0
          DG.add_edge(i, j, {'weight' : 0})
        else: #IF they represent different categories, the edge weight is 1
          DG.add_edge(i, j, {'weight' : 1})
      #THIS IS THE OVERFLOW NODE!!
      DG.add_edge(i, 2*k, {'weight' : 2})
    return DG

  def repair(self, DG): #new_feature = repair_feature(feature, create_graph(feature))
    mincostFlow = nx.max_flow_min_cost(DG, 's', 't') #max_flow_min_cost returns Dictionary of dictionaries. Keyed by nodes such that mincostFlow[u][v] is the flow edge (u,v)
    bin_dict = self.bin_fulldata
    index_dict = self.bin_index_dict_reverse
    size_data = len(self.data)
    repair_bin_dict = {}
    repair_data = [0]*size_data #initialize repaired data to be 0. If there are zero's after we fill it in the those observations belong in the overflow, "no category"
    k = self.num_bins
    overflow = 0
    for i in range(0,k): #for each lefthand side node i
      overflow += mincostFlow[i][2*k]
      for j in range(k, 2*k): #for each righthand side node j
        edgeflow = mincostFlow[i][j] #get the int (edgeflow) representing the amount of observations going from node i to j
        group = random.sample(bin_dict[i], int(edgeflow)) #randomly sample x (edgeflow) unique elements from the list of observations in that category.
        q=j-k #q is the category index for a righhand side node
        for elem in group: #for each element in the randomly selected group list
          bin_dict[i].remove(elem) #remove the element from the list of observation in that category
          repair_data[elem] = index_dict[q] #Mutate repair data at the index of the observation (elem) with its new category (it was 0) which is the category index for the righthand side node it flows to
        if q in repair_bin_dict: #if the category index is already keyed
          repair_bin_dict[q].extend(group) #extend the list of observations with a new list of observations in that category
        else:
          repair_bin_dict[q] = group #otherwise key that category index and set it's value as the group list in that category
    new_feature = CategoricalFeature(repair_data) #initialize our new_feature (repaired feature)
    new_feature.bin_fulldata = repair_bin_dict
    return [new_feature,overflow]

from itertools import product
from collections import defaultdict

from AbstractRepairer import AbstractRepairer

from collections import defaultdict
from copy import deepcopy

class Repairer(AbstractRepairer):
  def repair(self, data_to_repair):
    col_ids = range(len(data_to_repair[0]))

    # Get column type information
    col_types = ["Y"]*len(col_ids)
    for i, col in enumerate(col_ids):
      if i in self.features_to_ignore:
        col_types[i] = "I"
      elif i == self.feature_to_repair:
        col_types[i] = "X"
      else:
        continue

    col_type_dict = {col_id: col_type for col_id, col_type in zip(col_ids, col_types)}
    Y_col_ids = filter(lambda x: col_type_dict[x] == "Y", col_ids)
    not_I_col_ids = filter(lambda x: col_type_dict[x] != "I", col_ids)

    # To prevent potential perils with user-provided column names, map them to safe column names
    safe_stratify_cols = [self.feature_to_repair]

    # Extract column values for each attribute in data
    # Begin by initializing keys and values in dictionary
    data_dict = {col_id: [] for col_id in col_ids if col_id in Y_col_ids}
    
    # Populate each attribute with its column values
    for row in data_to_repair:
      for i in col_ids:
        if i in Y_col_ids:
          data_dict[i].append(row[i])


    # Create unique value structures:
    # When performing repairs, we choose median values. If repair is partial, then values will
    # be modified to some intermediate value between the original and the median value. However,
    # the partially repaired value will only be chosen out of values that exist in the data set.
    # This prevents choosing values that might not make any sense in the data's context.
    # To do this, for each column, we need to sort all unique values and create two data structures:
    # a list of values, and a dict mapping values to their positions in that list. Example:
    #   There are unique_col_vals[col] = [1, 2, 5, 7, 10, 14, 20] in the column. A value 2 must be
    #   repaired to 14, but the user requests that data only be repaired by 50%. We do this by
    #   finding the value at the right index:
    #   index_lookup[col][2] = 1; index_lookup[col][14] = 5; this tells us that
    #   unique_col_vals[col][3] = 7 is 50% of the way from 2 to 14.
    unique_col_vals = {}
    index_lookup = {}
    for col_id in not_I_col_ids:
      col_values = data_dict[col_id] #TODO: Make this use all_data
      # extract unique values from column and sort
      col_values = sorted(list(set(col_values)))
      unique_col_vals[col_id] = col_values
      # look up a value, get its position
      index_lookup[col_id] = {col_values[i]: i for i in range(len(col_values))}


    # Make a list of unique values per each stratified column.
    # Then make a list of combinations of stratified groups. Example: race and gender cols are stratified:
    # [(white, female), (white, male), (black, female), (black, male)]
    # The combinations are tuples because they can be hashed and used as dictionary keys.
    # From these, find the sizes of these groups.
    unique_stratify_values = [unique_col_vals[i] for i in safe_stratify_cols]
    all_stratified_groups = list(product(*unique_stratify_values))
    # look up a stratified group, and get a list of indices corresponding to that group in the data
    stratified_group_indices = defaultdict(list)
    # Find the sizes of each combination of stratified groups in the data
    sizes = {group: 0 for group in all_stratified_groups}
    for i in range(len(data_dict[safe_stratify_cols[0]])):
      group = tuple(data_dict[col][i] for col in safe_stratify_cols)
      stratified_group_indices[group].append(i)
      sizes[group] += 1

    # Don't consider groups not present in data (size 0)
    all_stratified_groups = filter(lambda x: sizes[x], all_stratified_groups)

    # Separate data by stratified group to perform repair on each Y column's values given that their
    # corresponding protected attribute is a particular stratified group. We need to keep track of each Y column's
    # values corresponding to each particular stratified group, as well as each value's index, so that when we
    # repair the data, we can modify the correct value in the original data. Example: Supposing there is a
    # Y column, "Score1", in which the 3rd and 5th scores, 70 and 90 respectively, belonged to black women,
    # the data structure would look like: {("Black", "Woman"): {Score1: [(70,2),(90,4)]}}
    stratified_group_data = {group: {} for group in all_stratified_groups}
    for group in all_stratified_groups:
      for col_id in data_dict:
        stratified_col_values = sorted([(data_dict[col_id][i], i) for i in stratified_group_indices[group]], key=lambda vals: vals[0])
        stratified_group_data[group][col_id] = stratified_col_values
    features = {}
    categories = {}
    categories_count = {}
    desired_categories_count = {}
    print data_dict 
    for col_id in data_dict:
      #data_dict[col_id] should be a list containing the values for all observations
      values = data_dict[col_id]
      feature = Feature(values, True)
      feature.categorize()
      bin_index_dict = feature.bin_index_dict
      print bin_index_dict
      categories[col_id] = []
      for key,value in bin_index_dict:
         categories[col_id].append(key)

    for group in all_stratified_groups:
      for col_id in data_dict:
        values = stratified_group_data[group][col_id]
        feature = Feature(values, True)
        feature.categorize()
        features[col_id][group] = feature.category_count
    for col_id in data_dict:
      for group in all_stratified_groups:
        category_count = features[col_id][group]
        for category in categories[col_id]:
          if category in category_count:
            categories_count[category][group] += category_count[category]
      for category in categories[col_id]:
        median = sorted(categories_count[category])[len(values_at_quantile)/2]
        desired_categories_count[category] = median
      for group in all_stratified_groups:
        feature = features[col_id][group]
        feature.desired_categories_count = desired_categories_count
        DG=create_graph(feature)
        new_feature = repair_feature(feature,DG)
 


class Feature:
  def __init__(self, data, categorical=False, name="no_name"):
    #data is an array of the data, with length n (# of observations)
    self.data = data
    #categorical is binary, True if categorical data 
    self.categorical = categorical
    #name of the feature column
    self.name = name
    #The following are initialized in categorize()
    #number of bins (number of categories)
    self.num_bins = None
    #bin_index_dict is type defaultdict(int), KEY: category, VALUE: category index
    self.bin_index_dict = None
    #bin_index_dict_reverse is type defaultdict(int), KEY: category index, VALUE: category
    self.bin_index_dict_reverse = None
    #bin data is type defaultdict(int), Key: category index, VALUE: number of observations with that category
    self.bin_data = None
    #bin full data is type defaultdict(list), Key: category index, VALUE: array of indices i, where data[i] is in that category
    
    self.bin_fulldata = None
    #The following are initialized in repair()
    #bin_data_repaired is type defaultdict(int), Key: category index, VALUE: number of desired observations with that category 
    self.bin_data_repaired = None
    self.desired_category_count = None

    self.category_count=None
    
  def categorize(self):
    if self.categorical: 
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
    else:
      print "error: not categorical data"

  def repair(self, repaird_data={}, protected_attribute =[]): #We have to make a design choice here (discussion in README)
    if (not self.bin_data): self.categorize() #checks to make the feature has run through categorize()
    else:
      d = deepcopy(self.bin_data) #deepcopy ensures that self.bin_data does not get mutated
      sumvals=0
      for key, value in d.items(): #we get the number of observations
        sumvals += value
      avgval = sumvals/len(d.items()) #divide number of observations by number of categorues
      remainder = sumvals % len(d.items()) 
      for key, value in d.items(): #evenly distribute the number of observations across categories
        if remainder > 0:
          d[key] = avgval +1
          remainder -= 1
        else:
          d[key] = avgval   
      self.bin_data_repaired = d #This is our temporary desired distribution (number of observation in each category)

def test():
  all_data = [ 
  ["x","A"],
  ["x","A"],
  ["x","B"],
  ["x","B"],
  ["x","B"],
  ["y","A"],
  ["y","A"],
  ["y","A"],
  ["y","B"],
  ["z","A"],
  ["z","A"],
  ["z","A"],
  ["z","A"],
  ["z","A"],
  ["z","B"]]
  #feature_to_repair is really feature to repair ON
  feature_to_repair = 0
  repair_level=1
  repairer = Repairer(all_data, feature_to_repair, repair_level)
  print repairer.repair(all_data)

if __name__== "__main__":
  test()

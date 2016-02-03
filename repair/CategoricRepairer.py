from itertools import product
from collections import defaultdict

from AbstractRepairer import AbstractRepairer
from CategoricalFeature import CategoricalFeature
from calculators import get_median

import random
import math
from copy import deepcopy

class Repairer(AbstractRepairer):
  def repair(self, data_to_repair):
    col_ids = get_col_ids(data_to_repair)

    # Get column type information
    col_types = ["Y"]*len(col_ids)
    for i, col in enumerate(col_ids):
      if i in self.features_to_ignore:
        col_types[i] = "I"
      elif i == self.feature_to_repair:
        col_types[i] = "X"

    col_type_dict = {col_id: col_type for col_id, col_type in zip(col_ids, col_types)}

    not_I_col_ids = filter(lambda x: col_type_dict[x] != "I", col_ids)
    cols_to_repair = filter(lambda x: col_type_dict[x] == "Y", col_ids)

    # To prevent potential perils with user-provided column names, map them to safe column names
    safe_stratify_cols = [self.feature_to_repair]

    # Extract column values for each attribute in data
    # Begin by initializing keys and values in dictionary
    data_dict = {col_id: [] for col_id in col_ids}

    # Populate each attribute with its column values
    for row in data_to_repair:
      for i in col_ids:
        data_dict[i].append(row[i])


    repair_types = {}
    for col_id, values in data_dict.items():
      if all(isinstance(value, float) for value in values):
        repair_types[col_id] = float
      elif all(isinstance(value, int) for value in values):
        repair_types[col_id] = int
      else:
        repair_types[col_id] = str

    """
     Create unique value structures: When performing repairs, we choose median values. If repair is partial, then values will be modified to some intermediate value between the original and the median value. However, the partially repaired value will only be chosen out of values that exist in the data set.  This prevents choosing values that might not make any sense in the data's context.  To do this, for each column, we need to sort all unique values and create two data structures: a list of values, and a dict mapping values to their positions in that list. Example: There are unique_col_vals[col] = [1, 2, 5, 7, 10, 14, 20] in the column. A value 2 must be repaired to 14, but the user requests that data only be repaired by 50%. We do this by finding the value at the right index:
       index_lookup[col][2] = 1
       index_lookup[col][14] = 5
       this tells us that unique_col_vals[col][3] = 7 is 50% of the way from 2 to 14.
    """
    unique_col_vals = {}
    index_lookup = {}
    for col_id in not_I_col_ids:
      col_values = data_dict[col_id] #TODO: Make this use all_data
      # extract unique values from column and sort
      col_values = sorted(list(set(col_values)))
      unique_col_vals[col_id] = col_values
      # look up a value, get its position
      index_lookup[col_id] = {col_values[i]: i for i in range(len(col_values))}

    """
     Make a list of unique values per each stratified column.  Then make a list of combinations of stratified groups. Example: race and gender cols are stratified: [(white, female), (white, male), (black, female), (black, male)] The combinations are tuples because they can be hashed and used as dictionary keys.  From these, find the sizes of these groups.
    """
    unique_stratify_values = [unique_col_vals[i] for i in safe_stratify_cols]
    all_stratified_groups = list(product(*unique_stratify_values))
    # look up a stratified group, and get a list of indices corresponding to that group in the data
    stratified_group_indices = defaultdict(list)

    # Find the number of unique values for each strat-group, organized per column.
    val_sets = {group: {col_id:set() for col_id in cols_to_repair}
                                     for group in all_stratified_groups}
    for i, row in enumerate(data_to_repair):
      group = tuple(row[col] for col in safe_stratify_cols)
      for col_id in cols_to_repair:
        val_sets[group][col_id].add(row[col_id])

      # Also remember that this row pertains to this strat-group.
      stratified_group_indices[group].append(i)

    # Sum the number of unique values present across each stratified group.
    sizes = {group: min(len(val_set) for _, val_set in val_sets[group].items()) for group in all_stratified_groups}

    # Don't consider groups not present in data (ie, size 0).
    all_stratified_groups = filter(lambda x: sizes[x], all_stratified_groups)

    """
     Separate data by stratified group to perform repair on each Y column's values given that their corresponding protected attribute is a particular stratified group. We need to keep track of each Y column's values corresponding to each particular stratified group, as well as each value's index, so that when we repair the data, we can modify the correct value in the original data. Example: Supposing there is a Y column, "Score1", in which the 3rd and 5th scores, 70 and 90 respectively, belonged to black women, the data structure would look like: {("Black", "Woman"): {Score1: [(70,2),(90,4)]}}
    """
    stratified_group_data = {group: {} for group in all_stratified_groups}
    for group in all_stratified_groups:
      for col_id, col_dict in data_dict.items():
        # Get the indices at which each value occurs.
        indices = {}
        for i in stratified_group_indices[group]:
          value = col_dict[i]
          if value not in indices:
            indices[value] = []
          indices[value].append(i)

        stratified_col_values = [(occurs, val) for val, occurs in indices.items()]
        stratified_col_values.sort(key=lambda tup: tup[1])
        stratified_group_data[group][col_id] = stratified_col_values

    # Find the combination with the fewest data points. This will determine what the quantiles are.
    num_quantiles = min(filter(lambda x: x, sizes.values())) # Remove any 0s
    quantile_unit = 1.0/num_quantiles

    # Init data dictionaries
    group_features = {}
    categories = {}
    categories_count = {}
    desired_categories_count = {}
    desired_categories_dist = {}
    group_size = {}
    categories_count_norm = {}
    distribution = {}

    # Repair Data and retrieve the results
    for col_id in cols_to_repair:
      # which bucket value we're repairing
      group_offsets = {group: 0 for group in all_stratified_groups}
      col = data_dict[col_id]

      if repair_types[col_id] in {int, float}:
        for quantile in range(num_quantiles):
          median_at_quantiles = []
          indices_per_group = {}

          for group in all_stratified_groups:
            offset = int(round(group_offsets[group]*sizes[group]))
            number_to_get = int(round((group_offsets[group] + quantile_unit)*sizes[group]) - offset)
            group_offsets[group] += quantile_unit

            # Get data at this quantile from this Y column such that stratified X = group
            group_data_at_col = stratified_group_data[group][col_id]
            offset_data = group_data_at_col[offset:offset+number_to_get]
            indices_per_group[group] = [i for val_indices, _ in offset_data for i in val_indices]
            values = sorted([float(val) for _, val in offset_data])

            # Find this group's median value at this quantile
            median_at_quantiles.append( get_median(values) )

          # Find the median value of all groups at this quantile (chosen from each group's medians)
          median = get_median(median_at_quantiles)
          median_val_pos = index_lookup[col_id][median]

          # Update values to repair the dataset.
          for group in all_stratified_groups:
            for index in indices_per_group[group]:
              original_value = col[index]

              current_val_pos = index_lookup[col_id][original_value]
              distance = median_val_pos - current_val_pos # distance between indices
              distance_to_repair = int(round(distance * self.repair_level))
              index_of_repair_value = current_val_pos + distance_to_repair
              repaired_value = unique_col_vals[col_id][index_of_repair_value]

              # Update data to repaired valued
              data_dict[col_id][index] = repaired_value

      #Categorical Repair is done below
      elif repair_types[col_id] in {str}:
        feature = CategoricalFeature(col)
        categories[col_id] = get_categories(feature.bin_index_dict)
        group_features[col_id], group_size[col_id] = get_group_data(all_stratified_groups, stratified_group_data, col_id)
        categories_count[col_id] = get_categories_count(categories, all_stratified_groups, col_id, group_features)
        categories_count_norm[col_id] = get_categories_count_norm(categories, col_id, all_stratified_groups, categories_count, group_size)
        median = get_median_per_category(categories, col_id, categories_count_norm)

        desired_categories_count[col_id],desired_categories_dist[col_id] = \
          get_desired_data(all_stratified_groups, col_id, categories, median, group_size, self.repair_level, categories_count_norm, categories_count)

        group_features[col_id], overflow = flow_on_group_features(all_stratified_groups, col_id, group_features, desired_categories_count)

        group_features[col_id], assigned_overflow, distribution[col_id] = assign_overflow(desired_categories_dist, all_stratified_groups, categories, col_id, overflow, group_features)

        # Return our repaired feature in the form of our original dataset
        for group in all_stratified_groups:
          indices = stratified_group_indices[group]
          for i, index in enumerate(indices):
            repaired_value = (group_features[col_id][group].data)[i]
            data_dict[col_id][index] = repaired_value

    # Replace stratified groups with their mode value, to remove it's information
    repaired_data = []
    mode = get_mode([row[self.feature_to_repair] for row in data_to_repair])
    for i, orig_row in enumerate(data_to_repair):
      new_row = [orig_row[j] if j in self.features_to_ignore else data_dict[j][i] for j in col_ids]

      # Replace the "feature_to_replace" column with the mode value.
      if self.repair_level > 0:
        new_row[self.feature_to_repair] = mode

      repaired_data.append(new_row)
    return repaired_data

def get_col_ids(data_to_repair):
  return range(len(data_to_repair[0]))

def get_categories(bin_index_dict):
  list = []
  for key,value in bin_index_dict.items():
    list.append(key)
  return list

def getKey(item):
    return item[0]
def get_group_data(all_stratified_groups,stratified_group_data, col_id):
  group_features={}
  group_size={}
  for group in all_stratified_groups:
    #stratified_group_data is a dictionary in the form: {('y',):{0: [([5,6,7,8],'A'])], 1: [([0,1,2,3,4]), 'B'])]}}
    list = stratified_group_data[group][col_id]
    points=[]
    values=[]
    for tuple in list:
      for i in tuple[0]:
        points.append((i, tuple[1]))
    points = sorted(points, key=getKey)
    for i in range(len(points)):
      (index, value) = points[i]
      values.append(value)
    # send values to CategoricalFeature object, which bins the data into categories
    group_features[group] = CategoricalFeature(values)
    group_size[group] = len(group_features[group].data)
  return group_features, group_size

# Count the observations in each category. e.g. categories_count[1] = {'A':[1,2,3], 'B':[3,1,4]}, for column 1, category 'A' has 1 observation from group 'x', 2 from 'y', ect.
def get_categories_count(categories, all_stratified_groups, col_id, group_features):
  dict={category: [] for category in categories[col_id]}
  for group in all_stratified_groups:
    category_count = group_features[col_id][group].category_count
    for category in categories[col_id]:
      count = category_count[category] if category in category_count else 0
      dict[category].append(count)
  return dict

# Find the normalized count for each category, where normalized count is count divided by the number of people in that group
def get_categories_count_norm(categories, col_id, all_stratified_groups, categories_count, group_size):
  norm = deepcopy(categories_count[col_id])
  for category in categories[col_id]:
    for i in range(len(norm[category])):
      group= all_stratified_groups[i]
      if group_size[col_id][group]==0: norm[category][i] = 0.0
      else: norm[category][i] = norm[category][i]* (1.0/group_size[col_id][group])
  return norm

# Find the median normalized count for each category
def get_median_per_category(categories, col_id, categories_count_norm):
  return {cat: get_median(categories_count_norm[col_id][cat]) for cat in categories[col_id]}

# Find the desired category count for each group, by using the repair_level (lambda). Desired category count is the desired distribution multiplied by the total number of observations in the group
def get_desired_data(all_stratified_groups, col_id, categories, median, group_size, repair_level, categories_count_norm, categories_count):
  dict1={}
  dict2={}
  for i, group in enumerate(all_stratified_groups):
    dict1[group] = {}
    dict2[group] = {}
    for category in categories[col_id]:
      med=median[category]
      size = group_size[col_id][group]
      # desired-proportion = (1-lambda)*original-count  + (lambda)*median-count
      count = categories_count[col_id][category][i]
      estimate = math.floor(((1-repair_level)*count)+(repair_level)*med*size)
      temp=((1 - repair_level)*categories_count_norm[col_id][category][i]) + (repair_level*med)
      # our desired-count = floor(desired-proportion * group-size)
      dict1[group][category] = estimate
      dict2[group][category] = temp
  return dict1, dict2

 # Run Max-flow to distribute as many observations to categories as possible. Overflow are those observations that are left over
def flow_on_group_features(all_stratified_groups, col_id, group_features, desired_categories_count):
  dict1= {}
  dict2={}
  for group in all_stratified_groups:
    feature = group_features[col_id][group]
    feature.desired_category_count = desired_categories_count[col_id][group]
    # Create directed graph from nodes that supply the original countes to nodes that demand the desired counts, with a overflow node as total desired count is at most total original counts
    DG=feature.create_graph()
    # Run max-flow, and record overflow count (total and per-group)
    new_feature,overflow = feature.repair(DG)
    dict2[group] = overflow
    # Update our original values with the values from max-flow, Note: still missing overflowed observations
    dict1[group] = new_feature
  return dict1, dict2

# Assign overflow observations to categories based on the group's desired distribution
def assign_overflow(desired_dists, all_stratified_groups, categories, col_id, overflow, group_features):
  feature = deepcopy(group_features[col_id])
  assigned_overflow = {}
  desired_dict_list = {}
  for group in all_stratified_groups:
    cat_props = [desired_dists[col_id][group][cat] for cat in categories[col_id]]
    if all(elem==0 for elem in cat_props): #TODO: Check that this is correct!
      cat_props = [1.0/len(cat_props)] * len(cat_props)
    s = float(sum(cat_props))
    for i, elem in enumerate(cat_props):
      cat_props[i] = elem/s
    desired_dict_list[group] = cat_props
    assigned_overflow[group] = {}
    for i in range(int(overflow[group])):
      distribution_list = desired_dict_list[group]
      number = random.uniform(0, 1)
      cat_index = 0
      tally = 0
      for j in range(len(distribution_list)):
        value=distribution_list[j]
        if number < (tally+value):
          cat_index = j
          break
        tally += value
      assigned_overflow[group][i] = categories[col_id][cat_index]
    # Actually do the assignment
    count = 0
    for i, value in enumerate(group_features[col_id][group].data):
      if value ==0:
        (feature[group].data)[i] = assigned_overflow[group][count]
        count += 1
  return feature, assigned_overflow, desired_dict_list

def get_mode(values):
  counts = {}
  for value in values:
    counts[value] = 1 if value not in counts else counts[value]+1
  mode_tuple = max(counts.items(), key=lambda tup: tup[1])
  return mode_tuple[0]


def test():
  test_minimal()
  test_get_group_data()
  test_get_categories_count()
  test_get_categories_count_norm()
  test_get_median_per_category()
  test_get_desired_data()
  test_assign_overflow()
  test_categorical()
  test_repeated_values()
  test_arrests()

def test_repeated_values():
  #TODO: Add this test (which is why Ricci broke originally)
  print "NEED TO ADD TEST FOR REPEATED VALUES IN CATEGORICAL REPAIR!", False

def test_minimal():
  class_1 = [[float(i),"A"] for i in xrange(0, 100)]
  class_2 = [[float(i),"B"] for i in xrange(101, 200)] # Thus, "A" is mode class.
  data = class_1 + class_2

  feature_to_repair = 1
  repairer = Repairer(data, feature_to_repair, 0.5)
  repaired_data = repairer.repair(data)
  print "Minimal Dataset -- repaired_data altered?", repaired_data != data

  mode = get_mode([row[feature_to_repair] for row in data])
  print "Minimal Dataset -- mode is true mode?", mode=="A"
  print "Minimal Dataset -- mode value as feature_to_repair?", all(row[feature_to_repair] == mode for row in repaired_data)

def test_get_group_data():
  group_features = {}
  group_size = {}
  col_id = 1
  all_stratified_groups = [('y',),('z',)]
  stratified_group_data = {('y',): {1: [([4, 7, 5], 'A'),([3, 2, 6], 'B'), ([], 'C')]},\
                           ('z',): {1: [([9, 1, 10], 'A'), ([], 'B'), ([11], 'C')]}}
  group_features[col_id], group_size[col_id] = get_group_data(all_stratified_groups, stratified_group_data, col_id)
  print "Test get_group_data -- group features correct?", \
    [group_features[col_id][group].data for group in all_stratified_groups] == [['B','B','A','A','B','A'],['A', 'A', 'A', 'C']]
  print "Test get_group_data -- group sizes correct?", group_size[col_id] == {('y',): 6, ('z',):4}

def test_get_categories_count():
  categories_count = {}
  categories = {1:['A','B','C','D']}
  all_stratified_groups = [('y',),('z',)]
  col_id = 1
  group_features = {1:{('y',): CategoricalFeature(['C','A','C','B','A','C']),\
                      ('z',): CategoricalFeature(['B','B','D','D'])}}\

  categories_count[col_id] = get_categories_count(categories, all_stratified_groups, col_id, group_features)
  print "Test get_categories_count -- category counts correct?",\
    categories_count[col_id] == {'A':[2,0],'B':[1,2], 'C':[3,0], 'D':[0,2]}

def test_get_categories_count_norm():
  categories_count_norm = {}
  categories = {1:['A','B']}
  all_stratified_groups = [('y',),('z',)]
  col_id = 1
  categories_count = {1: {'A':[4,0],'B':[16,0]}}
  group_size = {1: {('y',): 20,('z',): 0}}

  categories_count_norm[col_id] = get_categories_count_norm(categories, col_id, all_stratified_groups, categories_count, group_size)
  print "Test get_categories_count_norm -- normalized category counts correct?",\
    categories_count_norm[col_id] == {'A':[0.2,0.0],'B':[0.8,0.0]}

def test_get_median_per_category():
  categories = {1:['A','B','C','D']}
  col_id =1
  categories_count_norm = {1:{'A':[0.25,0.0],'C':[0.3,0.0],'B':[0.4,0.0],  'D':[0.6,0.4]}}
  median = get_median_per_category(categories, col_id, categories_count_norm)
  print "Test get_median_per_category -- medians are correct?", median == {'A':0.0,'C':0.0,'B':0.0,  'D':0.4}

def test_get_desired_data():
  desired_categories_count={}
  desired_categories_dist={}
  all_stratified_groups = [('y',),('z',)]
  col_id =1
  categories = {1:['A','B']}
  median = {'A':0.5,'B':0.5}
  group_size = {1: {('y',): 4,('z',): 8}}
  repair_level = 0.5
  categories_count_norm = {1:{'A':[0.5,0.5],'B':[0.5,0.5]}}
  categories_count = {1:{'A':[2, 4],'B':[2,4]}}

  desired_categories_count[col_id],desired_categories_dist[col_id] = \
      get_desired_data(all_stratified_groups, col_id, categories, median, group_size, repair_level, categories_count_norm, categories_count)
  print "Test get_desired_data -- Desired category counts correct?", \
    desired_categories_count[col_id] =={('y',):{'A':2.0, 'B':2.0}, ('z',):{'A':4.0,'B':4.0}}
  print "Test get_desired_data -- Desired category distribution correct?", \
    desired_categories_dist[col_id] == {('y',):{'A':0.5, 'B':0.5}, ('z',):{'A':0.5, 'B':0.5}}

def test_assign_overflow():
  random.seed(10)

  assigned_overflow={}
  distribution = {}
  group_features = {}
  desired_categories_dist = {1:{('y',):{'A':0.5,'B':0.5}, ('z',):{'A':0.0,'B':1.0}}}
  all_stratified_groups = [('y',),('z',)]
  categories = {1:['A','B']}
  col_id = 1
  overflow = {('y',):2,('z',):2}
  group_features = {1: {('y',):CategoricalFeature(['A','A','B','B',0,0]), ('z',): CategoricalFeature(['B',0,0])}}
  group_features[col_id], assigned_overflow, distribution[col_id] = assign_overflow(desired_categories_dist, all_stratified_groups, categories, col_id, overflow, group_features)
  print "Test assign_overflow -- updated group features correct?",\
    [group_features[col_id][group].data for group in all_stratified_groups] == [['A','A','B','B','B','A'],['B','B','B']]
  print "Test assign_overflow -- assigned overflow correctly?", assigned_overflow =={('y',): {0: 'B', 1: 'A'}, ('z',): {0: 'B', 1: 'B'}}
  print "Test assign_overflow -- distribution correct?", distribution[col_id] =={('y',): [0.5, 0.5], ('z',): [0.0, 1.0]}

def test_categorical():
  all_data = [
  ["x","A"], ["x","A"], ["x","B"], ["x","B"], ["x","B"],
  ["y","A"], ["y","A"], ["y","A"], ["y","B"],
  ["z","A"], ["z","A"], ["z","A"], ["z","A"], ["z","A"], ["z","B"]]

  random.seed(10)

  repair_level=1
  feature_to_repair = 0
  repairer = Repairer(all_data, feature_to_repair, repair_level)
  repaired_data=repairer.repair(all_data)

  correct_repaired_data = [
  ["z","A"], ["z","A"], ["z","B"], ["z","A"], ["z","A"],
  ["z","A"], ["z","A"], ["z","A"], ["z","B"],
  ["z","A"], ["z","A"], ["z","A"], ["z","A"], ["z","B"], ["z","B"]]

  print "Categorical Minimal Dataset -- full repaired_data altered?", repaired_data != all_data
  print "Categorical Minimal Dataset -- full repaired_data correct?", repaired_data == correct_repaired_data

  repair_level=0.1
  feature_to_repair = 0
  repairer = Repairer(all_data, feature_to_repair, repair_level)
  part_repaired_data=repairer.repair(all_data)

  correct_part_repaired_data = [
  ["z","A"], ["z","A"], ["z","B"], ["z","B"], ["z","A"],
  ["z","A"], ["z","A"], ["z","A"], ["z","B"],
  ["z","A"], ["z","A"], ["z","A"], ["z","A"], ["z","A"], ["z","B"]]

  print "Categorical Minimal Dataset -- partial repaired_data altered?", part_repaired_data != all_data
  print "Categorical Minimal Dataset -- partial repaired_data correct?", part_repaired_data == correct_part_repaired_data


def test_arrests():
  from experiments.arrests.load_data import load_data
  feature_to_repair = 0
  repair_level = 1.0
  _, train_data, test_data = load_data()

  repairer = Repairer(train_data+test_data, feature_to_repair, repair_level)
  repaired_data = repairer.repair(test_data)

  print "Arrest Dataset -- no rows lost?", len(repaired_data) == len(test_data)
  print "Arrest Dataset -- features changed for repair level '{}'? {}".format(repair_level, repaired_data != test_data)

  repair_level = 0.0
  repairer = Repairer(train_data+test_data, feature_to_repair, repair_level)
  repaired_data = repairer.repair(test_data)
  print "Arrest Dataset -- features not changed for repair level 0?", repaired_data == test_data
  if repaired_data != test_data: #TODO: Remove this after debugging.
    count = 0
    for rep,orig in zip(repaired_data, test_data):
      if rep != orig:
        print "wroooong: ", count, "------------------------",
        for i,j in zip(rep, orig):
          if i!=j: print j, "-->", i
        count += 1


if __name__== "__main__":
  test()

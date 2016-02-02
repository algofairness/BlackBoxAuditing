# NOTE:These settings and imports should be the only things that change
#       across experiments on different datasets
# TODO: Make this file generalizable to all datasets  

from experiments.arrests.load_data import load_data
from repair.CategoricRepairer import Repairer

import matplotlib.pyplot as plt
def run():
  feature_to_repair = 0
  repair_level = 1.0
  _, train_data, test_data = load_data()
  orig_data = train_data
  repairer = Repairer(orig_data, feature_to_repair, repair_level)
  repaired_data = repairer.repair(test_data)
  
  features_to_graph = range(1, 13)
  for feature_to_graph in features_to_graph:
    orig_groups = {}
    group_indices = {}
    for i, row in enumerate(orig_data):
      stratified_val = row[feature_to_repair]
      feature_val = row[feature_to_graph]
      if not stratified_val in orig_groups:
        orig_groups[stratified_val] = []
        group_indices[stratified_val] =[]
      orig_groups[stratified_val].append(feature_val)
      group_indices[stratified_val].append(i)
    rep_groups = {group:[repaired_data[i][feature_to_graph] for i in indices] for group, indices in group_indices.items()}
    for group, data in orig_groups.items():
      data_dict = {value: 0 for value in data}
      for value in data:
        data_dict[value] += 1
      id=1
      data_list = []
      for value, count in data_dict.items():
        data_list.extend([id]*count)
        id += 1
      plt.hist(data_list, bins=range(50))
      plt.savefig("figures/"+ str(feature_to_graph)+ "_original_" + group + ".png")
      plt.clf()
    for group, data in rep_groups.items():
      data_dict = {value: 0 for value in data}
      for value in data:
        data_dict[value] += 1
      id=1
      data_list = []
      for value, count in data_dict.items():
        data_list.extend([id]*count)
        id += 1
      plt.hist(data_list, bins=range(50))
      plt.savefig("figures/"+ str(feature_to_graph)+ "_repaired_" + group + ".png")
      plt.clf()
    
  
if __name__=="__main__":
  run()


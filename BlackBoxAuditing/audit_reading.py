import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import json
import os, shutil
import random
import csv
from os import listdir
from os.path import isfile, join
import matplotlib
matplotlib.use('Agg') # Set the back-end
import matplotlib.pyplot as plt


def load_audit_confusion_matrices(filename):
  """
  Loads a confusion matrix in a two-level dictionary format.

  For example, the confusion matrix of a 75%-accurate model
  that predicted 15 values (and mis-classified 5) may look like:
  {"A": {"A":10, "B": 5}, "B": {"B":5}}

  Note that raw boolean values are translated into strings, such that
  a value that was the boolean True will be returned as the string "True".
  """

  with open(filename) as audit_file:
    next(audit_file) # Skip the first line.

    # Extract the confusion matrices and repair levels from the audit file.
    confusion_matrices = []
    for line in audit_file:
      separator = ":"
      separator_index = line.index(separator)

      comma_index = line.index(',')
      repair_level = float(line[separator_index+2:comma_index])
      raw_confusion_matrix = line[comma_index+2:-2]
      confusion_matrix = json.loads( raw_confusion_matrix.replace("'","\"") )
      confusion_matrices.append( (repair_level, confusion_matrix) )

  # Sort the repair levels in case they are out of order for whatever reason.
  confusion_matrices.sort(key = lambda pair: pair[0])
  return confusion_matrices


def graph_audit(filename, measurers, output_image_file, write_to_file=True, print_all_data=False, feature=None, confusion_matrices=None):
  if not write_to_file and (feature == None or confusion_matrices == None):
    raise Exception("if write_to_file is False, additional data must be provided")

  if write_to_file:
    with open(filename) as audit_file:
      header_line = audit_file.readline()[:-1] # Remove the trailing endline.
    confusion_matrices = load_audit_confusion_matrices(filename)
  else:
    header_line = "GFA Audit for: " + feature

  x_axis = [repair_level for repair_level, _ in confusion_matrices]
  y_axes = []

  # Graph the results for each requested measurement.
  for measurer in measurers:
    y_axis = [measurer(matrix) for _, matrix in confusion_matrices]
    plt.plot(x_axis, y_axis, label=measurer.__name__)
    y_axes.append(y_axis)

  # Format and save the graph to an image file.
  plt.title(header_line)
  plt.axis([0,1,0,1.1]) # Make all the plots consistently sized.
  plt.xlabel("Repair Level")
  plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
  if write_to_file:
    plt.savefig(output_image_file, bbox_inches='tight')
  else:
    plt.show()
  plt.clf() # Clear the entire figure so future plots are empty.

  # Save the data used to generate that image file.
  if write_to_file:
    with open(output_image_file + ".data", "w") as f:
      writer = csv.writer(f)
      headers = ["Repair Level"] + [calc.__name__ for calc in measurers]
      writer.writerow(headers)
      for i, repair_level in enumerate(x_axis):
        writer.writerow([repair_level] + [y_vals[i] for y_vals in y_axes])
  elif print_all_data:
    print(feature + "Data")
    for i, repair_level in enumerate(x_axis):
      print([repair_level] + [y_vals[i] for y_vals in y_axes])


def get_data_from_file(file_dir):
  with open(file_dir) as f:
    reader = csv.reader(f)
    data = [row for row in reader]
    headers = data.pop(0)

  numerical_features = []
  categorical_features = {}
  for i, row in enumerate(data):
    for j, val in enumerate(row):
      try:
        val = int(val)
        data[i][j] = val
      except:
        try:
          val = float(val)
          data[i][j] = val
        except:
          pass

  return data, headers

def get_num_and_cat_feats(data):
  numerical_features = []
  categorical_features = {}
  for i, row in enumerate(data):
    for j, val in enumerate(row):
      if i == 0:
        if type(val) == int or type(val) == float:
          numerical_features.append(j)
        else:
          categorical_features[j] = [val]
      else:
        if j in categorical_features and not val in categorical_features[j]:
          categorical_features[j].append(val)

  return numerical_features, categorical_features

# Graphs Distributions for all combinations of categorical and numerical features
def graph_distributions(directory, file, response_header, write_to_file=True, rep_feat_index=None, test_data=None, repaired_data=None, headers=None, rep_lev=""):
  if not write_to_file and (rep_feat_index == None or test_data == None or repaired_data == None or headers == None or rep_lev == ""):
    raise Exception("if write_to_file is False, additional data must be provided")

  # gest the test and repaired data, and the repaired feature index
  if write_to_file:
    test_data, headers = get_data_from_file(directory + "/" + "original_test_data.csv")
    repaired_data, _ = get_data_from_file(directory + "/" + file)
    # uses the filename to get the repaired feature index
    rep_feat_index = headers.index(file.split(".")[0])

  # gets numerical and categorical features
  numerical_features, categorical_features = get_num_and_cat_feats(test_data)

  # if its repaired for a numerical feature, exit and move on to the next file
  if not rep_feat_index in categorical_features:
    return

  # create distributions for the different groups and their repaired variants
  for num_feat in numerical_features:
    if headers[num_feat] == response_header:
      return
    #initialize test_to_graph and repaired_to_graph, which will hold the data to be graphed for each group
    test_to_graph = {group:[] for group in categorical_features[rep_feat_index]}
    repaired_to_graph = {group:[] for group in categorical_features[rep_feat_index]}
    #goes through each row, adding the data to the correct group for both repaired and test data
    for i, row in enumerate(test_data):
      for group in categorical_features[rep_feat_index]:
        if row[rep_feat_index] == group:
          test_to_graph[group].append(row[num_feat])
          repaired_to_graph[group].append(repaired_data[i][num_feat])

    #create and save/show graph
    for group in test_to_graph:
      test_final = test_to_graph[group]
      repaired_final = repaired_to_graph[group]
      #Add a bit of noise to keep seaborn from breaking
      test_final = [float(val) for val in test_final]
      test_final = [(val + 0.00001*random.randint(1, 1000)) for val in test_final]
      repaired_final = [float(val) for val in repaired_final]
      repaired_final = [(val + 0.00001*random.randint(1, 1000)) for val in repaired_final]
      sns.distplot(test_final, hist=False, label=group, axlabel = headers[num_feat])
      sns.distplot(repaired_final, hist=False, label=("Reapired " + group))
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title("{} vs {} Distribution {}".format(headers[rep_feat_index], headers[num_feat], rep_lev))
    if write_to_file:
      plt.savefig(directory + "/" + headers[num_feat] + "_" + (str(file)).replace(".","_") + "_Distribution", bbox_inches='tight')
    else:
      plt.show()
    plt.clf()


# Graphs Distributions for a particular repaired and numerical feature, only showing some groups if desired
def graph_particular_distribution(directory, file, num_feat_index, only_groups=None, rfi=None):
  #only_groups should be in the form of ["group1", "group2", ect] or [("group1", repaired?), ("group2", repaired?), ect]
  #rfi is the index of the repaired feature, to be used if the data isnt 100% repaired

  if not "1.0.data" in file and rfi == None:
    print("If data is not completely repaired, you must specify the repaired index")
    return
  if "1.0.data" in file:
    rfi = None

  #fill test_data with the data in the file
  test_data_filename = directory + "/" + "unrepaired_test_data"    
  with open(test_data_filename) as f:
    reader = csv.reader(f)
    test_data = [row for row in reader]
  
  #fill repaired_data with the data in the file
  repaired_data_filename = directory + "/" + file
  with open(repaired_data_filename) as f:
    reader = csv.reader(f)
    repaired_data = [row for row in reader]
    headers = repaired_data.pop(0)

  #set the values to the correct types
  for i, row in enumerate(repaired_data):
    for j, val in enumerate(row):
      try:
        repaired_data[i][j] = int(val)
      except:
        try:
          repaired_data[i][j] = float(val)
        except:
          pass

  if rfi == None:
    #find the feature the file is repaired for 
    rep_feat_TF  = [True]*len(repaired_data[0])
    for i, row in enumerate(repaired_data):
      if i == 0:
        last_vals = row
      for j, val in enumerate(row):
        if last_vals[j] != val:
          rep_feat_TF[j] = False
      last_vals = row
    rep_feat_index = rep_feat_TF.index(True)
  else:
    rep_feat_index = rfi

  #set the values to the correct types and get the groups for the repaired feature
  groups = []
  no_repaired = []
  for i, row in enumerate(test_data):
    for j, val in enumerate(row):
      try:
        val = int(val)
        test_data[i][j] = val
      except:
        try:
          val = float(val)
          test_data[i][j] = val
        except:
          pass
      if only_groups == None:
        if j == rep_feat_index and not val in groups:
          groups.append(val)
      elif not type(only_groups[0]) == type((0, 0)):
        groups = only_groups
      else:
        for g in only_groups:
          if not g[0] in groups:
            groups.append(g[0])
          if g[1] == False:
            no_repaired.append(g[0])
      #print(groups)

  #initialize test_to_graph and repaired_to_graph, which will hold the data that will be graphed
  test_to_graph = {i:[] for i, _ in enumerate(groups)}
  repaired_to_graph = {i:[] for i, _ in enumerate(groups)}
  #goes through each row, adding the data to the correct group for both repaired and test data
  for i, row in enumerate(test_data):
    for group in groups:
      if row[rep_feat_index] == group:
        test_to_graph[groups.index(group)].append(row[num_feat_index])
        repaired_to_graph[groups.index(group)].append(repaired_data[i][num_feat_index])

  #create and save graph
  i = 0
  while i < len(test_to_graph):
    t = test_to_graph[i]
    r = repaired_to_graph[i]
    #Add a bit of noise to keep seaborn from breaking
    t = [float(n) for n in t]
    t = [(n + 0.00001*random.randint(1, 1000)) for n in t]
    r = [float(n) for n in r]
    r = [(n + 0.00001*random.randint(1, 1000)) for n in r]
    sns.distplot(t, hist=False, label=groups[i], axlabel = headers[num_feat_index])
    if not groups[i] in no_repaired:
      sns.distplot(r, hist=False, label=("Repaired " + groups[i]))
    i += 1
  #generate figname
  figname = directory + "/" + (str(file)).replace(".","_") + ":" + headers[rep_feat_index] + "_" + headers[num_feat_index]
  if not only_groups == None:
    for g in groups:
      figname += "_" + g
      if g in no_repaired:
        figname += "-no_rep"
  figname += "_Distribution"
  plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
  plt.title("{} vs {} Distribution".format(headers[rep_feat_index], headers[num_feat_index]))
  plt.savefig(figname, bbox_inches='tight')
  plt.clf()


def graph_audits(filenames_or_cm_all_feat, measurer, output_image_file, write_to_file=True, print_all_data=False):
  # if write_to_file is True, filenames_or_cm_all_feat will be a list of filenames to rank. otherwise, it will be a list of the conf matrices for all features
  features = []
  y_axes = []
  for filename_or_feature in filenames_or_cm_all_feat:
    if write_to_file:
      with open(filename_or_feature) as audit_file:
        header_line = audit_file.readline()[:-1] # Remove the trailing endline.
        feature = header_line[header_line.index(":")+1:]
      confusion_matrices = load_audit_confusion_matrices(filename_or_feature)
    else:
      feature = filename_or_feature
      confusion_matrices = filenames_or_cm_all_feat[feature]

    x_axis = [repair_level for repair_level, _ in confusion_matrices]
    y_axis = [measurer(matrix) for _, matrix in confusion_matrices]
    plt.plot(x_axis, y_axis, label=feature)

    features.append(feature)
    y_axes.append(y_axis)

  # Format and save the graph to an image file.
  plt.title(measurer.__name__)
  plt.axis([0,1,0,1.1]) # Make all the plots consistently sized.
  plt.xlabel("Repair Level")
  plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
  if write_to_file:
    plt.savefig(output_image_file, bbox_inches='tight')
  else:
    plt.show()
  plt.clf() # Clear the entire figure so future plots are empty.

  # Save the data used to generate that image file.
  if write_to_file:
    with open(output_image_file + ".data", "w") as f:
      writer = csv.writer(f)
      headers = ["Repair Level"] + features
      writer.writerow(headers)
      for i, repair_level in enumerate(x_axis):
        writer.writerow([repair_level] + [y_vals[i] for y_vals in y_axes])
  elif print_all_data:
    print(measurer.__name__ + " Data")
    headers = ["Repair Level"] + features
    print(headers)
    for i, repair_level in enumerate(x_axis):
      print([repair_level] + [y_vals[i] for y_vals in y_axes])


def rank_audit_files(filenames_or_cm_all_feat, measurer, write_to_file=True):
  # if write_to_file is True, filenames_or_cm_all_feat will be a list of filenames to rank. otherwise, it will be a list of the conf matrices for all features
  scores = []
  for filename_or_feature in filenames_or_cm_all_feat:
    if write_to_file:
      with open(filename_or_feature) as audit_file:
        header_line = audit_file.readline()[:-1] # Remove the trailing endline.
        feature = header_line[header_line.index(":")+1:]
        confusion_matrices = load_audit_confusion_matrices(filename_or_feature)
    else:
      feature = filename_or_feature
      confusion_matrices = filenames_or_cm_all_feat[feature]
    
    _, start_matrix = confusion_matrices[0]
    _, end_matrix = confusion_matrices[-1]
    score_difference = measurer(start_matrix)-measurer(end_matrix)
    scores.append( (feature, score_difference) )

  scores.sort(key = lambda score_tup: score_tup[1], reverse=True)
  return scores

def group_audit_ranks(filenames_or_cm_all_feat, measurer, similarity_bound=0.05, write_to_file=True):
  # if write_to_file is True, filenames_or_cm_all_feat will be a list of filenames to rank. otherwise, it will be a list of the conf matrices for all features

  """
  Given a list of audit files, rank them using the `measurer` and
  return the features that never deviate more than `similarity_bound`
  across repairs.
  """

  def _partition_groups(feature_scores):
    groups = []
    for feature, score in feature_scores:
      added_to_group = False

      # Check to see if the feature belongs in a group with any other features.
      for i, group in enumerate(groups):
        mean_score, group_feature_scores = group
        if abs(mean_score - score) < similarity_bound:
          groups[i][1].append( (feature, score) )

          # Recalculate the representative mean.
          groups[i][0] = sum([s for _, s in group_feature_scores])/len(group_feature_scores)
          added_to_group = True
          break

      # If this feature did not much with the current groups, create another group.
      if not added_to_group:
        groups.append( [score, [(feature,score)]] )

    # Return just the features.
    return [[feature for feature, score in group] for _, group in groups]


  score_dict = {}
  features = []
  for filename_or_feature in filenames_or_cm_all_feat:
    if write_to_file:
      with open(filename_or_feature) as audit_file:
        header_line = audit_file.readline()[:-1] # Remove the trailing endline.
        feature = header_line[header_line.index(":")+1:]
        features.append(feature)
      confusion_matrices = load_audit_confusion_matrices(filename_or_feature)
    else:
      feature = filename_or_feature
      features.append(filename_or_feature)
      confusion_matrices = filenames_or_cm_all_feat[filename_or_feature]
    
    for rep_level, matrix in confusion_matrices:
      score = measurer(matrix)
      if rep_level not in score_dict:
        score_dict[rep_level] = {}
      score_dict[rep_level][feature] = score

  # Sort by repair level increasing repair level.
  score_keys = sorted(score_dict.keys())
  groups = [features]
  while score_keys:
    key = score_keys.pop()
    new_groups = []
    for group in groups:
      group_features = [(f, score_dict[key][f]) for f in group]
      sub_groups = _partition_groups(group_features)
      new_groups.extend(sub_groups)
    groups = new_groups

  return groups


def test():
  TMP_DIR = "tmp"
  if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

  test_contents = "GFA Audit for: Test Feature\n0.0.data:[0.0, {'A': {'B': 100}, 'B': {'B': 199}}]\n0.1.data:[0.1, {'A': {'B': 100}, 'B': {'B': 199}}]\n0.5.data:[0.5, {'A': {'B': 100}, 'B': {'B': 199}}]\n1.0.data:[1.0, {'A': {'B': 100}, 'B': {'B': 199}}]\n"
  test_filenames = [TMP_DIR + "/test_audit_1.audit",
                    TMP_DIR + "/test_audit_2.audit"]

  # Prepare the sample audit files.
  for filename in test_filenames:
    with open(filename, "w") as f:
      f.write(test_contents)

  # A mock measurement measurer that returns a random number.
  def mock_measurer(conf_matrix):
    return random.random()

  # Perform the audit and save it an output image.
  measurers = [mock_measurer, mock_measurer]
  output_image = TMP_DIR + "/test_image.png"
  graph_audit(test_filenames[0], measurers, output_image) # Only need to test 1.

  file_not_empty = os.path.getsize(output_image) > 0
  print("image file generated? --", file_not_empty)

  file_not_empty = os.path.getsize(output_image + ".data") > 0
  print("data file generated? --", file_not_empty)

  ranked_features = rank_audit_files(test_filenames, mock_measurer)
  print("ranked features sorted? --", ranked_features[0] > ranked_features[1])

  output_image = TMP_DIR + "/test_image2.png"
  graph_audits(test_filenames, mock_measurer, output_image)
  file_not_empty = os.path.getsize(output_image) > 0
  print("ranked image file generated? --", file_not_empty)

  shutil.rmtree(TMP_DIR)

if __name__=="__main__":
  test()




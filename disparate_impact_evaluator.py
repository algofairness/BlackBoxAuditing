# NOTE: These settings and imports should be the only things that change
#       across experiments on different datasets and ML model types.
#'''
#Prices (gas) SVM
custom_title = "Gas Prices, SVM "
source = "audits/1458835147.37"
output1="disparate_impact_graphs/svm_Gas_DI_Accuracy"
axis1=[.95,1.05,.84,.9]
output2="disparate_impact_graphs/svm_Gas_DI_Simplarity_Predictions"
axis2=[.95,1.05,.94,1]
output3="disparate_impact_graphs/svm_Gas_RepairLevel_DI"
axis3=[0,1.0,0,1.1]
protected_groups = ["0","1"]
unprotected_group = "0"
race_feature = "asian_zip"
#'''
'''
#Prices (PR with gas) SVM
custom_title = "Princeton Review Prices, SVM "
source = "audits/1458834701.09"
output1="disparate_impact_graphs/svm_PR_DI_Accuracy"
axis1=[.95,1.05,.84,.9]
output2="disparate_impact_graphs/svm_PR_DI_Simplarity_Predictions"
axis2=[.95,1.05,.94,1]
output3="disparate_impact_graphs/svm_PR_RepairLevel_DI"
axis3=[0,1.0,0,1.1]
protected_groups = ["0","1"]
unprotected_group = "0"
race_feature = "asian_zip"
'''
'''
#Florida sor svm
custom_title = "Florida SOR, SVM "
source = "audits/1457121057.1"
output1="disparate_impact_graphs/svm_floridasor_DI_Accuracy"
axis1=[.95,1.05,.84,.9]
output2="disparate_impact_graphs/svm_floridasor_DI_Simplarity_Predictions"
axis2=[.95,1.05,.94,1]
output3="disparate_impact_graphs/svm_floridasor_RepairLevel_DI"
axis3=[0,1.0,.7,1.1]
protected_groups = ["W","B"]
unprotected_group = "W"
race_feature = "race"
#'''
'''
#Florida sor predrace SVM
custom_title = "Florida SOR-BSG, SVM "
source = "audits/1457121072.16"
output1="disparate_impact_graphs/svm_predrace_floridasor_DI_Accuracy"
axis1=[.9,1.05,.85,.92]
output2="disparate_impact_graphs/svm_predrace_floridasor_DI_Simplarity_Predictions"
axis2=[.9,1.05,.92,1.02]
output3="disparate_impact_graphs/svm_predrace_floridasor_RepairLevel_DI"
axis3=[0,1.0,.7,1.1]
protected_groups = ["WHITE","BLACK","HISPANIC"]
unprotected_group = "WHITE"
race_feature = "pred_race"
'''

'''
#sor j48
custom_title = "SOR, J48 "
source = "audits/1456373048.67"
output1="disparate_impact_graphs/j48_sor_DI_Accuracy"
axis1=[.85,1.1,.75,.85]
output2="disparate_impact_graphs/j48_sor_DI_Simplarity_Predictions"
axis2=[.85,1.1,.9,1.05]
output3="disparate_impact_graphs/j48_sor_RepairLevel_DI"
axis3=[0,1.0,.7,1.1]
protected_groups = ["White","Black", "American Indian or Alaskan Native", "Asian or Pacific Islander", "Unknown"]
unprotected_group = "White"
race_feature = "race"
'''
'''
#sor_no_unknown j48
custom_title = "SOR, J48, Ignore Unknown, "
source = "audits/1456439286.2"
output1="disparate_impact_graphs/j48_nounknown_sor_DI_Accuracy"
axis1=[.65,1.1,.65,.85]
output2="disparate_impact_graphs/j48_nounknown_sor_DI_Simplarity_Predictions"
axis2=[.65,1.1,.6,1.05]
output3="disparate_impact_graphs/j48_nounknown_sor_RepairLevel_DI"
axis3=[0,1,.6,1.1]
protected_groups = ["White","Black", "American Indian or Alaskan Native", "Asian or Pacific Islander"]
unprotected_group = "White"
race_feature = "race"
'''
'''
#sor_predrace j48
custom_title = "SOR-BISG, J48 "
source = "audits/1456377058.83"
output1="disparate_impact_graphs/j48_predrace_sor_DI_Accuracy"
axis1=[.85,1.1,.75,.85]
output2="disparate_impact_graphs/j48_predrace_sor_DI_Simplarity_Predictions"
axis2=[.85,1.1,.85,1.2]
output3="disparate_impact_graphs/j48_predrace_sor_RepairLevel_DI"
axis3=[0,1.0,.70,1.1]
protected_groups = ["WHITE","BLACK", "HISPANIC"]
unprotected_group = "WHITE"
race_feature = "pred_race"
'''
'''
#sor svm
custom_title = "SOR, SVM "
source = "audits/1456396585.66"
output1="disparate_impact_graphs/svm_sor_DI_Accuracy"
axis1=[.85,1.1,.75,.85]
output2="disparate_impact_graphs/svm_sor_DI_Simplarity_Predictions"
axis2=[.85,1.1,.85,1.1]
output3="disparate_impact_graphs/svm_sor_RepairLevel_DI"
axis3=[0,1.1,.70,1.1]
protected_groups = ["White","Black", "American Indian or Alaskan Native", "Asian or Pacific Islander", "Unknown"]
unprotected_group = "White"
race_feature = "race"
'''
'''
#arrests
custom_title = "Arrests, J48 "
source = "audits/1455586474.33"
output1="disparate_impact_graphs/j48_arrests_DI_Accuracy"
axis1=[.5,1.3,.5,.8]
output2="disparate_impact_graphs/j48_arrests_DI_Simplarity_Predictions"
axis2=[.5,1.3,.8,1.1]
output3="disparate_impact_graphs/j48_arrests_RepairLevel_DI"
axis3=[0,1,.4,1.4]
protected_groups = ["WHITE","BLACK", "UNKNOWN", "ASIAN/PACIFIC ISLANDER", "AMERICAN INDIAN/ALEUTIAN"]
unprotected_group = "WHITE"
race_feature = "RACE"
#'''
from disparate_impact import disparate_impact
from consistency_graph import *


from os import listdir
from os.path import isfile, join

def load_trip_from_predictions(filename):
  with open(filename) as f:
    reader = csv.reader(f)
    reader.next # Skip the headers.
    return [(f,r,p) for f,r,p in reader]

def accuracy(triples):
  matches = 0.0
  total = 0.0
  for _, orig, pred in triples:
    if orig == pred: 
      matches += 1
    total += 1

  return matches/total

def graph_disparate_impact_accuracy(directory, output_image_file):
  only_files = [f for f in listdir(directory) if isfile(join(directory, f))]
  preds = ["{}/{}".format(directory, f) for f in only_files if ".predictions" in f]

  delim = ".audit.repaired_"

  ignored = ["original_train_data.predictions", "original_test_data.predictions"]

  file_groups = {}
  for pred in preds:
    if any(i in pred for i in ignored): continue
    feature = pred[len(directory)+1:pred.index(delim)] # Extract the feature name.
    if feature not in file_groups:
      file_groups[feature] = []
    file_groups[feature].append(pred)

  pred_groups = {}
  for feature, filenames in file_groups.items():
    pred_groups[feature] = []
    for filename in filenames:
      preds = load_trip_from_predictions(filename)
      first_delim = filename.index(delim)+len(delim)
      second_delim = filename.index(".predictions")
      repair_level = float(filename[first_delim:second_delim])
      pred_groups[feature].append( (repair_level, preds) )
    pred_groups[feature].sort(key=lambda tup: tup[0]) # Sort by repair level.

  features = []
  y_axes = []
  for feature, pred_tups in pred_groups.items():
    if feature == race_feature:
      for protected_group in protected_groups:       
        x_axis = [disparate_impact(triples[1:], unprotected_group, protected_group) for _,triples in pred_tups] 
        y_axis = [accuracy(triples[1:]) for _, triples in pred_tups]
        plt.plot(x_axis, y_axis, label=protected_group)
        features.append(protected_group)
        y_axes.append(y_axis)

      # Format and save the graph to an image file.
      plt.title(custom_title + "Accuracy")
      plt.axis(axis1) # Make all the plots consistently sized.
      plt.xlabel("Disparate Impact: Pr(Good Outcome given Race = X) / Pr(Good Outcome given Race = WHITE)")
      plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
      plt.savefig(output_image_file, bbox_inches='tight')
      plt.clf() # Clear the entire figure so future plots are empty.

      # Save the data used to generate that image file.
      with open(output_image_file + ".data", "w") as f:
        writer = csv.writer(f)
        headers = ["Disparate Impact"] + features
        writer.writerow(headers)
        for i, repair_level in enumerate(x_axis):
          writer.writerow([repair_level] + [y_vals[i] for y_vals in y_axes])

def graph_disparate_impact_similarity_predictions(directory, output_image_file):
  only_files = [f for f in listdir(directory) if isfile(join(directory, f))]
  preds = ["{}/{}".format(directory, f) for f in only_files if ".predictions" in f]

  delim = ".audit.repaired_"

  ignored = ["original_train_data.predictions", "original_test_data.predictions"]

  file_groups = {}
  for pred in preds:
    if any(i in pred for i in ignored): continue
    feature = pred[len(directory)+1:pred.index(delim)] # Extract the feature name.
    if feature not in file_groups:
      file_groups[feature] = []
    file_groups[feature].append(pred)

  pred_groups = {}
  for feature, filenames in file_groups.items():
    pred_groups[feature] = []
    for filename in filenames:
      preds = load_trip_from_predictions(filename)
      first_delim = filename.index(delim)+len(delim)
      second_delim = filename.index(".predictions")
      repair_level = float(filename[first_delim:second_delim])
      pred_groups[feature].append( (repair_level, preds) )
    pred_groups[feature].sort(key=lambda tup: tup[0]) # Sort by repair level.

  features = []
  y_axes = []
  for feature, pred_tups in pred_groups.items():
    if feature == race_feature:
      for protected_group in protected_groups:
        #TODO clean this bit of code up, it's hacky right now
        real_pred_tups=[]
        for repair_level, triples in pred_tups:
          tups = []
          for triple in triples:
            tups.append((triple[1],triple[2]))
          real_pred_tups.append((repair_level,tups))
        
        orig = []
        for triple in pred_tups[0][1]:
          orig.append((triple[1],triple[2]))
        
        x_axis = [disparate_impact(triples[1:], unprotected_group, protected_group) for _,triples in pred_tups] 
        y_axis = [similarity_to_original_preds(orig, tups) for _, tups in real_pred_tups]
        plt.plot(x_axis, y_axis, label=protected_group)
        features.append(protected_group)
        y_axes.append(y_axis)

      # Format and save the graph to an image file.
      plt.title(custom_title + "Similarity to Original Predictions")
      plt.axis(axis2) # Make all the plots consistently sized.
      plt.xlabel("Disparate Impact: Pr(Good Outcome given Race = X) / Pr(Good Outcome given Race = WHITE)")
      plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
      plt.savefig(output_image_file, bbox_inches='tight')
      plt.clf() # Clear the entire figure so future plots are empty.

      # Save the data used to generate that image file.
      with open(output_image_file + ".data", "w") as f:
        writer = csv.writer(f)
        headers = ["Disparate Impact"] + features
        writer.writerow(headers)
        for i, repair_level in enumerate(x_axis):
          writer.writerow([repair_level] + [y_vals[i] for y_vals in y_axes])

def graph_repair_level_disparate_impact(directory, output_image_file):
  only_files = [f for f in listdir(directory) if isfile(join(directory, f))]
  preds = ["{}/{}".format(directory, f) for f in only_files if ".predictions" in f]

  delim = ".audit.repaired_"

  ignored = ["original_train_data.predictions", "original_test_data.predictions"]

  file_groups = {}
  for pred in preds:
    if any(i in pred for i in ignored): continue
    feature = pred[len(directory)+1:pred.index(delim)] # Extract the feature name.
    if feature not in file_groups:
      file_groups[feature] = []
    file_groups[feature].append(pred)

  pred_groups = {}
  for feature, filenames in file_groups.items():
    pred_groups[feature] = []
    for filename in filenames:
      preds = load_trip_from_predictions(filename)
      first_delim = filename.index(delim)+len(delim)
      second_delim = filename.index(".predictions")
      repair_level = float(filename[first_delim:second_delim])
      pred_groups[feature].append( (repair_level, preds) )
    pred_groups[feature].sort(key=lambda tup: tup[0]) # Sort by repair level.

  features = []
  y_axes = []
  for feature, pred_tups in pred_groups.items():
    if feature == race_feature:
      for protected_group in protected_groups:
        #TODO Figure out how to categorize feature values
        x_axis = [rep_level for rep_level,_ in pred_tups]
        #y_axis = [similarity_to_original_preds(orig, tups) for _, tups in pred_tups]
        y_axis = [disparate_impact(triples[1:], unprotected_group, protected_group) for _,triples in pred_tups]    
        #triples[0] = (Pre-Repaired Feature,Response,Prediction)
        #triples[1] = (WHITE,1,1)
        plt.plot(x_axis, y_axis, label=protected_group)
        features.append(protected_group)
        y_axes.append(y_axis)

      # Format and save the graph to an image file.
      plt.title(custom_title + "Disparate Impact: Pr(Good Outcome given Race = X) / Pr(Good Outcome given Race = WHITE)")
      plt.axis(axis3) # Make all the plots consistently sized.
      plt.xlabel("Repair Level")
      plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
      plt.savefig(output_image_file, bbox_inches='tight')
      plt.clf() # Clear the entire figure so future plots are empty.

      # Save the data used to generate that image file.
      with open(output_image_file + ".data", "w") as f:
        writer = csv.writer(f)
        headers = ["Repair Level"] + features
        writer.writerow(headers)
        for i, repair_level in enumerate(x_axis):
          writer.writerow([repair_level] + [y_vals[i] for y_vals in y_axes])

if __name__=="__main__":
  graph_disparate_impact_accuracy(source, output1)
  graph_disparate_impact_similarity_predictions(source, output2)
  graph_repair_level_disparate_impact(source, output3)

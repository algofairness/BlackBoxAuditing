# NOTE: These settings and imports should be the only things that change
#       across experiments on different datasets and ML model types.

options = ["gas prices", "pr prices without gas", "pr prices with gas", "sor", "sor_predrace", "arrests", "arrests svm",\
"gas prices j48", "pr prices without gas j48", "pr prices with gas j48", "sor j48", "sor_predrace j48"]
#experiment="gas prices"
def get_source(experiment):
  if experiment == "gas prices j48":
    #Prices (gas) J48( 27705.pts-19.cook)
    custom_title = "Gas Prices, J48 "
    source = "audits/1460440466.09"
    output0="disparate_impact_graphs/3b_j48_Gas_Accuracy"
    output1="disparate_impact_graphs/3b_j48_Gas_DI_Accuracy"
    axis1=[.45,1.05,.625,.78]
    output2="disparate_impact_graphs/3b_j48_Gas_DI_Simplarity_Predictions"
    axis2=[.2,1.05,.5,1.1]
    output3="disparate_impact_graphs/3b_j48_Gas_RepairLevel_DI"
    axis3=[0,1.0,0,1.1]
    protected_groups = ["0","1"]
    unprotected_group = "0"
    race_feature = "asian_zip"

  if experiment == "pr prices without gas j48":
    #Prices (PR without gas) J48 (10719.pts-2.fried)
    custom_title = "PR Prices without Gas Price, J48 "
    source = "audits/1460440283.36"
    output0="disparate_impact_graphs/2b_j48_PR_Accuracy"
    output1="disparate_impact_graphs/2b_j48_PR_DI_Accuracy"
    axis1=[.4,1.05,.7,.82]
    output2="disparate_impact_graphs/2b_j48_PR_DI_Simplarity_Predictions"
    axis2=[.2,1.05,.5,1.1]
    output3="disparate_impact_graphs/2b_j48_PR_RepairLevel_DI"
    axis3=[0,1.0,0,1.1]
    protected_groups = ["0","1"]
    unprotected_group = "0"
    race_feature = "asian_zip"

  if experiment == "pr prices with gas j48":
    #Prices (PR with gas) J48 (23653.pts-2.fried)
    custom_title = "PR Prices with Gas Price, J48 "
    source = "audits/1460440412.52" 
    output0="disparate_impact_graphs/4b_j48_PR_gas_Accuracy"
    output1="disparate_impact_graphs/4b_j48_PR_gas_DI_Accuracy"
    axis1=[.3,1.05,.7,.82]
    output2="disparate_impact_graphs/4b_j48_PR_gas_DI_Simplarity_Predictions"
    axis2=[.2,1.05,.5,1.1]
    output3="disparate_impact_graphs/4b_j48_PR_gas_RepairLevel_DI"
    axis3=[0,1.0,0,1.1]
    protected_groups = ["0","1"]
    unprotected_group = "0"
    race_feature = "asian_zip"

  if experiment == "sor j48":
    #Georgia sor TRUERACE j48 28811.pts-19.cook
    custom_title = "SOR using True Race, J48 "
    source = "audits/1460440872.03"
    output0="disparate_impact_graphs/5b_j48_sor_truerace_Accuracy"
    output1="disparate_impact_graphs/5b_j48_sor_truerace_DI_Accuracy"
    axis1=[.7,1.1,.9,.96]
    output2="disparate_impact_graphs/5b_j48_sor_truerace_DI_Simplarity_Predictions"
    axis2=[.6,1.5,.6,1.1]
    output3="disparate_impact_graphs/5b_j48_sor_truerace_RepairLevel_DI"
    axis3=[0,1.1,.8,1.2]
    protected_groups = ["White","Black", "American Indian or Alaskan Native", "Asian or Pacific Islander", "Unknown"]
    unprotected_group = "White"
    race_feature = "race"

  if experiment == "sor_predrace j48":
    #Georgia sor PREDRACE j48 29151.pts-28.pearl
    custom_title = "SOR using Predicted Race, J48 "
    source = "audits/1460441005.61"
    output0="disparate_impact_graphs/6b_svm_sor_predrace_Accuracy"
    output1="disparate_impact_graphs/6b_svm_sor_predrace_DI_Accuracy"
    axis1=[.9,1.05,.91,.94]
    output2="disparate_impact_graphs/6b_svm_sor_predrace_DI_Simplarity_Predictions"
    axis2=[.6,1.5,.6,1.1]
    output3="disparate_impact_graphs/6b_svm_sor_predrace_RepairLevel_DI"
    axis3=[0,1.1,.86,1.05]
    protected_groups = ["White","Black", "Hispanic","American Indian or Alaskan Native", "Asian or Pacific Islander", "Other"]
    unprotected_group = "White"
    race_feature = "pred_race"

  if experiment == "arrests svm":
    #arrests  (29261.pts-28.pearl)
    custom_title = "Arrests, SVM "
    source = "audits/1460477456.42"
    output0="disparate_impact_graphs/1a_svm_arrests_Accuracy"
    output1="disparate_impact_graphs/1a_svm_arrests_DI_Accuracy"
    axis1=[.6,1.3,.65,.69]
    output2="disparate_impact_graphs/1a_svm_arrests_DI_Simplarity_Predictions"
    axis2=[.5,1.3,.8,1.1]
    output3="disparate_impact_graphs/1a_svm_arrests_RepairLevel_DI"
    axis3=[0,1,.4,1.4]
    protected_groups = ["WHITE","BLACK", "UNKNOWN", "ASIAN/PACIFIC ISLANDER", "AMERICAN INDIAN/ALEUTIAN"]
    unprotected_group = "WHITE"
    race_feature = "RACE"


  if experiment == "gas prices":
    #Prices (gas) SVM 
    custom_title = "Gas Prices, SVM "
    source = "audits/1459310114.24"
    output0="disparate_impact_graphs/3a_svm_Gas_Accuracy"
    output1="disparate_impact_graphs/3a_svm_Gas_DI_Accuracy"
    axis1=[.2,1.05,.6,.78]
    output2="disparate_impact_graphs/3a_svm_Gas_DI_Simplarity_Predictions"
    axis2=[.2,1.05,.5,1.1]
    output3="disparate_impact_graphs/3a_svm_Gas_RepairLevel_DI"
    axis3=[0,1.0,0,1.1]
    protected_groups = ["0","1"]
    unprotected_group = "0"
    race_feature = "asian_zip"

  if experiment == "pr prices without gas":
    #Prices (PR without gas) SVM 
    custom_title = "PR Prices without Gas Price, SVM "
    source = "audits/1459310172.2"
    output0="disparate_impact_graphs/2a_svm_PR_Accuracy"
    output1="disparate_impact_graphs/2a_svm_PR_DI_Accuracy"
    axis1=[.2,1.05,.7,.8]
    output2="disparate_impact_graphs/2a_svm_PR_DI_Simplarity_Predictions"
    axis2=[.2,1.05,.5,1.1]
    output3="disparate_impact_graphs/2a_svm_PR_RepairLevel_DI"
    axis3=[0,1.0,0,1.1]
    protected_groups = ["0","1"]
    unprotected_group = "0"
    race_feature = "asian_zip"

  if experiment == "pr prices with gas":
    #Prices (PR with gas) SVM 
    custom_title = "PR Prices with Gas Price, SVM "
    source = "audits/1459309973.86"
    output0="disparate_impact_graphs/4a_svm_PR_gas_Accuracy" 
    output1="disparate_impact_graphs/4a_svm_PR_gas_DI_Accuracy"
    axis1=[.3,1.05,.7,.85]
    output2="disparate_impact_graphs/4a_svm_PR_gas_DI_Simplarity_Predictions"
    axis2=[.2,1.05,.5,1.1]
    output3="disparate_impact_graphs/4a_svm_PR_gas_RepairLevel_DI"
    axis3=[0,1.0,0,1.1]
    protected_groups = ["0","1"]
    unprotected_group = "0"
    race_feature = "asian_zip"

  if experiment == "sor":
    #Georgia sor TRUERACE svm
    custom_title = "SOR using True Race, SVM "
    source = "audits/1459228686.97"
    output0="disparate_impact_graphs/5a_svm_sor_truerace_Accuracy"
    output1="disparate_impact_graphs/5a_svm_sor_truerace_DI_Accuracy"
    axis1=[.7,1.4,.71,.83]
    output2="disparate_impact_graphs/5a_svm_sor_truerace_DI_Simplarity_Predictions"
    axis2=[.6,1.5,.6,1.1]
    output3="disparate_impact_graphs/5a_svm_sor_truerace_RepairLevel_DI"
    axis3=[0,1.1,.6,1.5]
    protected_groups = ["White","Black", "American Indian or Alaskan Native", "Asian or Pacific Islander", "Unknown"]
    unprotected_group = "White"
    race_feature = "race"

  if experiment == "sor_predrace":
    #Georgia sor PREDRACE svm
    custom_title = "SOR using Predicted Race, SVM "
    source = "audits/1459229211.44"
    output0="disparate_impact_graphs/6a_svm_sor_predrace_Accuracy"
    output1="disparate_impact_graphs/6a_svm_sor_predrace_DI_Accuracy"
    axis1=[.89,1.35,.64,.74]
    output2="disparate_impact_graphs/6a_svm_sor_predrace_DI_Simplarity_Predictions"
    axis2=[.6,1.5,.6,1.1]
    output3="disparate_impact_graphs/6a_svm_sor_predrace_RepairLevel_DI"
    axis3=[0,1.1,.9,1.3]
    protected_groups = ["White","Black", "Hispanic","American Indian or Alaskan Native", "Asian or Pacific Islander", "Other"]
    unprotected_group = "White"
    race_feature = "pred_race"


  if experiment == "arrests":
    #arrests
    custom_title = "Arrests, J48 "
    source = "audits/1455586474.33"
    output0="disparate_impact_graphs/1b_j48_arrests_Accuracy"
    output1="disparate_impact_graphs/1b_j48_arrests_DI_Accuracy"
    axis1=[.5,1.3,.67,.71]
    output2="disparate_impact_graphs/1b_j48_arrests_DI_Simplarity_Predictions"
    axis2=[.5,1.3,.8,1.1]
    output3="disparate_impact_graphs/1b_j48_arrests_RepairLevel_DI"
    axis3=[0,1,.4,1.4]
    protected_groups = ["WHITE","BLACK", "UNKNOWN", "ASIAN/PACIFIC ISLANDER", "AMERICAN INDIAN/ALEUTIAN"]
    unprotected_group = "WHITE"
    race_feature = "RACE"
  
  return [custom_title, source,output0 , output1, output2, output3,axis1,axis2, axis3 ,  protected_groups, unprotected_group,race_feature] 

from disparate_impact import disparate_impact
from consistency_graph import *


from shutil import copyfile


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

def graph_accuracy(directory, output_image_file):
  copyfile(directory + "/accuracy.png", output_image_file)
  copyfile(directory + "/accuracy.png.data", output_image_file + ".csv")

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
      #plt.xlabel("Disparate Impact: Pr(Good Outcome given Race = X) / Pr(Good Outcome given Race = WHITE)")
      plt.xlabel("Disparate Impact")
      plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
      plt.savefig(output_image_file, bbox_inches='tight')
      plt.clf() # Clear the entire figure so future plots are empty.

      # Save the data used to generate that image file.
      with open(output_image_file + ".csv", "w") as f:
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
      #plt.xlabel("Disparate Impact: Pr(Good Outcome given Race = X) / Pr(Good Outcome given Race = WHITE)")
      plt.xlabel("Disparate Impact")
      plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
      plt.savefig(output_image_file, bbox_inches='tight')
      plt.clf() # Clear the entire figure so future plots are empty.

      # Save the data used to generate that image file.
      with open(output_image_file + ".csv", "w") as f:
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
      #plt.title(custom_title + "Disparate Impact: Pr(Good Outcome given Race = X) / Pr(Good Outcome given Race = WHITE)")
      plt.title(custom_title + "Disparate Impact")
      plt.axis(axis3) # Make all the plots consistently sized.
      plt.xlabel("Repair Level")
      plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
      plt.savefig(output_image_file, bbox_inches='tight')
      plt.clf() # Clear the entire figure so future plots are empty.

      # Save the data used to generate that image file.
      with open(output_image_file + ".csv", "w") as f:
        writer = csv.writer(f)
        headers = ["Repair Level"] + features
        writer.writerow(headers)
        for i, repair_level in enumerate(x_axis):
          writer.writerow([repair_level] + [y_vals[i] for y_vals in y_axes])

if __name__=="__main__":
  for option in options:
    [custom_title, source,output0 , output1, output2, output3,axis1,axis2, axis3 ,  protected_groups, unprotected_group,race_feature] = get_source(option)
    graph_accuracy(source, output0)
    graph_disparate_impact_accuracy(source, output1)
    #graph_disparate_impact_similarity_predictions(source, output2)
    graph_repair_level_disparate_impact(source, output3)

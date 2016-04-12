import csv
import math 
other_index = -2
split_by = "predator"

filename1 = "census_block/Georgia_confusionmatrix_final.csv"
truerace_index = 1
predrace_index = 0

def load_data():
  with open(filename1) as f:
    reader = csv.reader(f)
    data = [row for row in reader]
    headers = data.pop(0)
    print len(data)
    data = [row for row in data if all(elem!="" for elem in row)]
    print len(data)
  # These two are if we don't want to split on anything
  #data1 = [data[i][truerace_index] for i in range(len(data))]
  #data2 = [data[i][predrace_index] for i in range(len(data))]
  data3 = [data[i][other_index] for i in range(len(data))]
  data1 = [data[i][truerace_index] for i in range(len(data)) if data[i][other_index] == "1"]
  data2 = [data[i][predrace_index] for i in range(len(data)) if data[i][other_index] == "1"]
  print len(data1)
  print len(data2)
  print len(data3)
  list_of_dicts = []
  confusion_dict = {}
  for i, value1 in enumerate(data1):
  	confusion_dict[value1] = {}
  	for j, value2 in enumerate(data2):
  	  confusion_dict[value1][value2] = 0
  for i, value1 in enumerate(data1):
    value2 = data2[i]
    confusion_dict[value1][value2] += 1
  
  total = float(0)
  count = float(0)
  for value1 in confusion_dict:
    for value2 in confusion_dict[value1]:
      print "Actual: " + value1 + ", Predicted: " + value2 + ", Count: " + str(confusion_dict[value1][value2])
      total+=confusion_dict[value1][value2]
      if value1 == value2:
        count+=confusion_dict[value1][value2]

  accuracy = count/total

  print total
  
  confusion_dict2 ={}
  for value1 in confusion_dict:
    dict = {}
    dict['Split'] = "1"
    dict['True_Race'] = value1
    confusion_dict2[value1] ={}
    for value2 in confusion_dict[value1]:
      confusion_dict2[value1][value2] = math.floor(10000*(confusion_dict[value1][value2]/total))/100.0
      dict[value2] = str(confusion_dict[value1][value2])
      dict[value2+"-percent"] = confusion_dict2[value1][value2]
      dict["Accuracy"] = str(accuracy)
      #dict["Precision"] = str)
      #dict["BER"]
      #dict["Recall"] 
      list_of_dicts.append(dict)
  for value1 in confusion_dict2:
  	for value2 in confusion_dict2[value1]:
  		print "Actual: " + value1 + ", Predicted: " + value2 + ", Percent: " + str(confusion_dict2[value1][value2])

  print "Accuracy: " + str(accuracy)
  #print "Precision: " + str(accuracy)
  #print "Recall: " + str(accuracy)
  #data1 = [data[i][truerace_index] for i in range(len(data))]
  #data2 = [data[i][predrace_index] for i in range(len(data))]
  #data3 = [data[i][other_index] for i in range(len(data))]
  data1 = [data[i][truerace_index] for i in range(len(data)) if data[i][other_index] == "0"]
  data2 = [data[i][predrace_index] for i in range(len(data)) if data[i][other_index] == "0"]
  print len(data1)
  print len(data2)
  print len(data3)
  confusion_dict = {}
  for i, value1 in enumerate(data1):
    confusion_dict[value1] = {}
    for j, value2 in enumerate(data2):
      confusion_dict[value1][value2] = 0
  for i, value1 in enumerate(data1):
    value2 = data2[i]
    confusion_dict[value1][value2] += 1
  
  total = float(0)
  count = float(0)
  for value1 in confusion_dict:
    for value2 in confusion_dict[value1]:
      print "Actual: " + value1 + ", Predicted: " + value2 + ", Count: " + str(confusion_dict[value1][value2])
      total+=confusion_dict[value1][value2]
      if value1 == value2:
        count+=confusion_dict[value1][value2]

  accuracy = count/total

  print total
  
  confusion_dict2 ={}
  for value1 in confusion_dict:
    dict = {}
    dict['Split'] = "0"
    dict['True_Race'] = value1
    confusion_dict2[value1] ={}
    for value2 in confusion_dict[value1]:
      confusion_dict2[value1][value2] = math.floor(10000*(confusion_dict[value1][value2]/total))/100.0
      dict[value2] = str(confusion_dict[value1][value2])
      dict[value2+"-percent"] = confusion_dict2[value1][value2]
      dict["Accuracy"] = str(accuracy)
      #dict["Precision"] = str)
      #dict["BER"]
      #dict["Recall"] 
      list_of_dicts.append(dict)
  for value1 in confusion_dict2:
    for value2 in confusion_dict2[value1]:
      print "Actual: " + value1 + ", Predicted: " + value2 + ", Percent: " + str(confusion_dict2[value1][value2])

  print "Accuracy: " + str(accuracy)
  #print "Precision: " + str(accuracy)
  #print "Recall: " + str(accuracy)
  with open('disparate_impact_graphs/confusion_matrix_split_by_{}.csv'.format(split_by), 'w') as csvfile:
      fieldnames = ["Split","True_Race"]
      dict = {}
      for value2 in data2:
        dict[value2] = ""
      for value2 in dict:
        fieldnames.append(value2)
        fieldnames.append(value2 + "-percent")
      fieldnames.append("Accuracy")
      #fieldnames.append("Precision")
      #fieldnames.append("Recall")
      #fieldnames.append("BER")
      writer = csv.writer(csvfile)
      writer.writerow(fieldnames)
      for dict in list_of_dicts:
        writer.writerow([dict[fieldname] for fieldname in fieldnames])
if __name__=="__main__":
  load_data()

import csv
import math 

filename1 = "test_data/Florida_confusionmatrix.csv"
truerace_index = 0
predrace_index = 1
other_index = 6
def load_data():
  with open(filename1) as f:
    reader = csv.reader(f)
    data = [row for row in reader]
    headers = data.pop(0)
    print len(data)
    data = [row for row in data if all(elem!="" for elem in row)]
    print len(data)
  data1 = [data[i][truerace_index] for i in range(len(data))]
  data2 = [data[i][predrace_index] for i in range(len(data))]
  data3 = [data[i][other_index] for i in range(len(data))]
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

  for value1 in confusion_dict:
  	for value2 in confusion_dict[value1]:
  		print "Actual: " + value1 + ", Predicted: " + value2 + ", Count: " + str(confusion_dict[value1][value2])
  		total+=confusion_dict[value1][value2]
  print "Accuracy: " + str((confusion_dict["W"]["WHITE"] + confusion_dict["B"]["BLACK"] + confusion_dict["A"]["ASIAN"]+ confusion_dict["I"]["ASIAN PACIFIC ISLANDER"])/total)
  print total
  
  confusion_dict2 ={}
  for value1 in confusion_dict:
  	confusion_dict2[value1] ={}
  	for value2 in confusion_dict[value1]:
  		confusion_dict2[value1][value2] = math.floor(10000*(confusion_dict[value1][value2]/total))/100.0
  for value1 in confusion_dict2:
  	for value2 in confusion_dict2[value1]:
  		print "Actual: " + value1 + ", Predicted: " + value2 + ", Percent: " + str(confusion_dict2[value1][value2])


if __name__=="__main__":
  load_data()

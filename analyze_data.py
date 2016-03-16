from scipy import stats
import numpy as np
import csv
import math
filename1 = "audits/1456956355.93/pred_race.audit.repaired_0.0.predictions"
index1 = 1
index2 = 2
def load_data():
  with open(filename1) as f:
    reader = csv.reader(f)
    data = [row for row in reader]
    headers = data.pop(0)
    print len(data)
    data = [row[:7]+row[10:] for row in data]
    data = [row for row in data if all(elem!="" for elem in row)]
    print len(data)
  x = [int(data[i][index1]) for i in range(len(data))]
  y = [int(data[i][index2]) for i in range(len(data))]
  num = sum(y)
  num2 = sum(x)
  print "Response Sum",num2
  print "Prediction Sum",num
  slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
  print "r_value", r_value

load_data()
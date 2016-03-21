import csv
import random
def load_data():
  filename = "test_data/prices.csv"
  with open(filename) as f:
    reader = csv.reader(f)
    data = [row for row in reader]
    #data = [row[1:] for row in data]
    print len(data)
    data = [row for row in data if all(elem!="" for elem in row)]
    print len(data)
    headers = data.pop(0)
    print headers
    correct_types = [str,str, float, float, float, float]
    
    for i, row in enumerate(data):
      for j, correct_type in enumerate(correct_types):
        data[i][j] = correct_type(row[j])
    
    # Random sample to make response variable 50% "0"
    '''
    count =0
    indices0 = []
    indices1 = []
    for i,row in enumerate(data):
      if row[0] == "1":
        count += 1
        indices0.append(i)
      else:
        indices1.append(i)

    random_indices1 = random.sample(indices1, count)
    data1 = [row for i,row in enumerate(data) if i in indices0]
    data2 = [row for i,row in enumerate(data) if i in random_indices1]

    data = data1 + data2
    print len(data1)
    print len(data2)
    '''
    print len(data)
    
    ratio = 2/3
    random_sample = random.sample(range(len(data)), len(data)/3)
    train = [data[i] for i in range(len(data)) if i not in random_sample]
    test = [data[i] for i in random_sample]

    train = random.sample(train, len(train)/20) 
    test = random.sample(test, len(test)/20) 
  return headers, train, test


def test():
  headers, train, test = load_data()
  print "load_data unpacks correctly? -- ", (headers != None and train != None and test != None)

  correct_types = [str, str, float, float, float, float]
  gathered_types = []
  for i, header in enumerate(headers):
    if all( isinstance(row[i],float) for row in train + test ):
      gathered_types.append(float)
    elif all( isinstance(row[i],int) for row in train + test ):
      gathered_types.append(int)
    elif all( isinstance(row[i],str) for row in train + test ):
      gathered_types.append(str)

  print "load_data types are correct? -- ", gathered_types == correct_types


if __name__=="__main__":
  test()

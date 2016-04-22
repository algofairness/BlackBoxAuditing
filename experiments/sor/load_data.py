import csv
import random
def load_data():
  filename = "test_data/Georgia_truerace.csv"
  with open(filename) as f:
    reader = csv.reader(f)
    data = [row for row in reader]
    
    correct_types = [str, str, float, float, float, str, str, str, float, str, float, str, str, str, str]

    print len(data)
    print data[0]
    #getting rid of empty values and address features
    #data = [row[:7]+row[10:] for row in data]
    data = [row for row in data if all(elem!="" for elem in row)]
    for row in data:
      if len(row[9])>10:
        row[9] = row[9][0:10]
    print len(data)
    print data[1]
    headers = data.pop(0)
    for i, row in enumerate(data):
      for j, correct_type in enumerate(correct_types):
        data[i][j] = correct_type(row[j])

    ratio = 2/3
    random_sample = random.sample(range(len(data)), len(data)/3)
    train = [data[i] for i in range(len(data)) if i not in random_sample]
    test = [data[i] for i in random_sample]

    #train = random.sample(train, len(train)) 
    #test = random.sample(test, len(test)) 
  return headers, train, test



def test():
  headers, train, test = load_data()
  print "load_data unpacks correctly? -- ", (headers != None and train != None and test != None)

  correct_types = [str, str, float, float, float, str, str, str, float, str, float, str, str, str, str]
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

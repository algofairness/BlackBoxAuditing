import csv
import random
def load_data():
  filename = "test_data/Florida_predrace.csv"
  with open(filename) as f:
    reader = csv.reader(f)
    data = [row for row in reader]
    
    print len(data)
    print data[0]
    #getting rid of PERSON_NMB
    data = [row[:6]+row[7:] for row in data]
    data = [row for row in data if all(elem!="" for elem in row)]
    print len(data)
    headers = data.pop(0)
    print headers
    data = [row for row in data if all(elem!="Juvenile Sex Offender (Walsh)" for elem in row)]
    for i,row in enumerate(data):
      if row[10] == 'Offender':
        data[i][10] = '0'
      else:
        data[i][10] = '1'
    #Take out half of the non-predators...
    #print data[0]
    #data_nonpredator = [i for i,row in enumerate(data) if row[10] == '0']
    #data_predator = [i for i,row in enumerate(data) if row[10] == "1"]
    #print "Predators", len(data_predator)
    #print "nonPredators", len(data_nonpredator)
    #indices = random.sample(data_nonpredator, len(data_predator)) 
    #print len(indices)
    #indices.extend(data_predator)
    #data = [row for i,row in enumerate(data) if i in indices]
    print "Length", len(data)
    correct_types = [str, str, str, str, float, float, str, str, str, str, str]
    
    for i, row in enumerate(data):
      for j, correct_type in enumerate(correct_types):
        data[i][j] = correct_type(row[j])
    
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

  correct_types = [str, str, str, str, float, float, str, str, str, str, str]
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

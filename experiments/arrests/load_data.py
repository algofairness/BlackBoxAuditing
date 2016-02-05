import csv

def load_data():
  filename = "test_data/arrests_full_categorical.csv"
  with open(filename) as f:
    reader = csv.reader(f)
    data = [row for row in reader]
    headers = data.pop(0)

    correct_types = [str] * len(headers) # All categorical.

    for i, row in enumerate(data):
      for j, correct_type in enumerate(correct_types):
        data[i][j] = correct_type(row[j])

    train = data[:len(data)/2]
    test = data[len(data)/2:]

  return headers, train, test


def test():
  headers, train, test = load_data()
  print "load_data unpacks correctly? -- ", (headers != None and train != None and test != None)

  correct_types = [str] * len(headers)
  gathered_types = []
  for i, header in enumerate(headers):
    if all( isinstance(row[i],float) for row in train + test ):
      gathered_types.append(float)
    elif all( isinstance(row[i],int) for row in train + test ):
      gathered_types.append(int)
    elif all( isinstance(row[i],str) for row in train + test ):
      gathered_types.append(str)

  print "Test and train not empty? -- ", len(train)>0 and len(test)>0

  print "load_data types are correct? -- ", gathered_types == correct_types


if __name__=="__main__":
  test()



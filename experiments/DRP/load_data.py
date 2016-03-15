from splitters import split_by_percent
from collections import OrderedDict

train_filename = "test_data/DRP_old_train.arff"
test_filename = "test_data/DRP_old_test.arff"
response = "outcome"
train_percentage = 2.0/3.0

def load_data():
  header_types = OrderedDict()
  data = []
  with open(train_filename) as f:
    for line in f:
      if "@ATTRIBUTE" in line:
        _, header, arff_type = line.split()
        header_types[header] = float if arff_type=="NUMERIC" else str
      else:
        row = line[:-1].split(",") #TODO: This is a naive way of splitting, captain.
        row = [header_types[h](v) for h,v in zip(header_types, row)]
        data.append(row)

  with open(test_filename) as f:
    for line in f:
      if "@ATTRIBUTE" not in line:
        row = line[:-1].split(",") #TODO: This is a naive way of splitting, captain.
        row = [header_types[h](v) for h,v in zip(header_types, row)]
        data.append(row)

  headers = header_types.keys()

  # Translate the response into a binary.
  index = headers.index(response)
  translate = lambda row: row[:index] + ["1" if row[index] in "34" else "0"] + row[index+1:]
  data = map(translate, data)

  train, test = split_by_percent(data, train_percentage)

  return headers, train, test


def test():
  headers, train, test = load_data()
  print "load_data unpacks correctly? -- ", (headers != None and train != None and test != None)

  correct_types = [str, float, int, str, float, str]
  gathered_types = []
  for i, header in enumerate(headers):
    if all( isinstance(row[i],float) for row in train + test ):
      gathered_types.append(float)
    elif all( isinstance(row[i],int) for row in train + test ):
      gathered_types.append(int)
    elif all( isinstance(row[i],str) for row in train + test ):
      gathered_types.append(str)

  print "load_data types are correct? -- ", gathered_types == correct_types
  print "load_data count is correct? -- ", 3955 == len(train) + len(test)


if __name__=="__main__":
  test()



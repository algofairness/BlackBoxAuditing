from splitters import split_by_percent
import csv
from test_data import preloaded

def is_int(string):
  try:
    int(string)
    return True
  except ValueError:
    return False

def is_float(string):
  try:
    float(string)
    return True
  except ValueError:
    return False

def get_types(data,correct_types,empty_symbol):
  for i in range(len(correct_types)):
    row = 0
    while correct_types[i] is None:
      if data[row][i] == empty_symbol:
        row += 1
      else:
        if is_int(data[row][i]):
          correct_types[i] = int
        elif is_float[i] == float:
          correct_types[i] = float
        else:
          correct_types[i] = str

def load_data(data):
  if data not in preloaded:
    raise KeyError("{} is not an available dataset".format(data))
  if data == "DRP":
    return load_DRP(data)
  filename = preloaded[data]["filepath"]
  testdata = preloaded[data]["testdata"]
  correct_types = preloaded[data]["correct_types"]
  train_percentage = preloaded[data]["train_percentage"]
  response_header = preloaded[data]["response_header"]
  features_to_ignore = preloaded[data]["features_to_ignore"]
  with open(filename) as f:
    reader = csv.reader(f)
    data = [row for row in reader]
    headers = data.pop(0)

    for i, row in enumerate(data):
      for j, correct_type in enumerate(correct_types):
        data[i][j] = correct_type(row[j])

    if testdata is None:
      train, test = split_by_percent(data, train_percentage)
    else:
      train = data
      with open(testdata) as f:
        reader = csv.reader(f)
        test = [row for row in reader][1:] # Ignore headers.
  
        for i, row in enumerate(test):
          for j, correct_type in enumerate(correct_types):
            test[i][j] = correct_type(row[j])
  return headers, train, test, response_header, features_to_ignore


def load_DRP(data):
  train_filename = preloaded[data]["filepath"]
  test_filename = preloaded[data]["testdata"]
  train_percentage = preloaded[data]["train_percentage"]
  header = preloaded[data]["response_header"]
  features_to_ignore = preloaded[data]["features_to_ignore"]

  header_types = OrderedDict()
  data = []
  with open(train_filename) as f:
    for line in f:
      if "@attribute" in line:
        _, header, arff_type = line.split()
        header_types[header] = float if arff_type=="numeric" else str
      elif "@relation" in line or "@data" in line or line == "\n":
        pass
      else:
        row = line[:-1].split(",") #TODO: This is a naive way of splitting, captain.
        row = [header_types[h](v) for h,v in zip(header_types, row)]
        data.append(row)

  with open(test_filename) as f:
    for line in f:
      if "@attribute" not in line and "@relation" not in line and "@data" not in line and line != "\n":
        row = line[:-1].split(",") #TODO: This is a naive way of splitting, captain.
        row = [header_types[h](v) for h,v in zip(header_types, row)]
        data.append(row)

  headers = header_types.keys()

  train, test = split_by_percent(data, train_percentage)

  return headers, train, test, header, features_to_ignore


def load_from_file(datafile, testdata=None, correct_types=None, train_percentage=2.0/3.0,
                   response_header=None, features_to_ignore=None, missing_data_symbol=""):
  with open(datafile) as f:
    reader = csv.reader(f)
    data = [row for row in reader]
    headers = data.pop(0)

    # Set defaults in case they are not handed in as arguments
    if response_header is None:
      response_header = headers[-1]

    if features_to_ignore is None:
      features_to_ignore = []

    if correct_types is None:
	correct_types = get_types(data, [None]*len(headers), missing_data_symbol)
    
    for i, row in enumerate(data):
      for j, correct_type in enumerate(correct_types):
        data[i][j] = correct_type(row[j])

    if testdata is None:
      train, test = split_by_percent(data, train_percentage)
    else:
      train = data
      with open(testdata) as f:
        reader = csv.reader(f)
        test = [row for row in reader][1:] # Ignore headers.

        for i, row in enumerate(test):
          for j, correct_type in enumerate(correct_types):
            test[i][j] = correct_type(row[j])

  return headers, train, test, response_header, features_to_ignore

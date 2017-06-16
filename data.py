from splitters import split_by_percent
import csv

preloaded = {"adult":    {"filepath": "test_data/adult.csv",
                          "testdata": "test_data/adult.test.csv",
                          "correct_types": [int, str, int, str, int, str, str, str,
                                            str,str, int, int, int, str, str],
                          "train_percentage": None,
                          "response_header": "income-per-year",
                          "features_to_ignore": []},

             "diabetes": {"filepath": "test_data/pima-indians-diabetes.csv",
                          "testdata": None,
                          "correct_types": [int, float, float, float, float, 
                                            float, float, int, str],
                          "train_percentage": 1.0/2.0,
                          "response_header": "Class",
                          "features_to_ignore": []},

             "ricci":    {"filepath": "test_data/RicciDataMod.csv",
                          "testdata": None,
                          "correct_types": [str,float,int,str,float,str],
                          "train_percentage": 1.0/2.0,
                          "response_header": "Class",
                          "features_to_ignore":[]},

             "german":   {"filepath": "test_data/german_categorical.csv",
                          "testdata": None,
                          "correct_types": [str, int, str, str, int, str, str, int, str, str, int, 
                                            str, int, str, str, str, int, str, int, str, str, str],
                          "train_percentage": 2.0/3.0,
                          "response_header": "class",
                          "features_to_ignore": ["age"]},

             "glass":    {"filepath": "test_data/glass.csv",
                          "testdata": None,
                          "correct_types": [int, float, float, float, float, float, float, float,
                                            float, float, str],
                          "train_percentage": 1.0/2.0,
                          "response_header": "type of glass",
                          "features_to_ignore": []},

             "sample":   {"filepath": "test_data/sample.csv",
                          "testdata": None,
                          "correct_types": [int, int, int, int, float, str],
                          "train_percentage":2.0/3.0,
                          "response_header": "Outcome",
                          "features_to_ignore": []}
             }

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

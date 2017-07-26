import csv

from repairers.GeneralRepairer import Repairer

def kddtest(kdd):
  input_csv = 'test_data/RicciDataMod.csv'
  repair_level = 1.0
  protected_cols = ['Race']
  ignored = ['Position']

  with open(input_csv) as f:
    data = [line for line in csv.reader(f)]
    headers = data.pop(0)
    cols = [[row[i] for row in data] for i,col in enumerate(headers)]

    # Convert integer features to integers and float features to floats.
    for i, col in enumerate(cols):
      try:
        cols[i] = list(map(int, col))
      except ValueError:
        try:
          cols[i] = list(map(float, col))
        except ValueError:
          pass

    data = [[col[j] for col in cols] for j in range(len(data))]
    firstdata = data

  # Calculate the indices to repair by and to ignore.
  for protected in protected_cols:
    try:
      index_to_repair = headers.index(protected)
    except ValueError as e:
      raise Exception("Response header '{}' was not found in the following headers: {}".format(protected, headers))

    try:
      ignored_features = [headers.index(feature) for feature in ignored] if ignored else []
    except ValueError as e:
      raise Exception("One or more ignored-features were not found in the headers: {}".format(headers))

    repairer = Repairer(data, index_to_repair,
                        repair_level, kdd, features_to_ignore=ignored_features)


    # Repair the input data.
    data = repairer.repair(data)

    if not kdd:
      with open('repair_tests/RicciRepair1.0.KDDflag.csv') as f:
        correct_data = [line for line in csv.reader(f)]
    else:
      with open('repair_tests/RicciRepair1.0.noKDDflag.csv') as f:
        correct_data = [line for line in csv.reader(f)]

    # This is gross and I'm so sorry.
    strdata = []
    for line in data:
      for x in range(len(line)):
        line[x] = str(line[x])    
      strdata.append(line)

    if strdata == correct_data:
      return True
    else:
      return False

def test():
  print("Correct results for regular repair algorithm? -- ", kddtest(False))
  print("Correct results for KDD algorithm? -- ", kddtest(True))

if __name__ == "__main__": test()

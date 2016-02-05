from splitters import split_by_percent
import csv
import random

str_headers = ["boolean_crystallisation_outcome_manual_0"]
ignored_headers = ["notes", "rxnSpaceHash1_drpxxhash_0.02/0.4.3","reaction_ptr",
                   "labGroup", "user", "insertedDateTime", "performedDateTime",
                   "performedBy", "reference", "recommendation", "id",
                   "compound_0", "compound_0_role","compound_1", "compound_1_role",
                   "compound_2", "compound_2_role","compound_3", "compound_3_role",
                   "compound_4", "compound_4_role", "duplicateOf",
                   "crystallisation_outcome_manual_0",
                   "legacyRecommendedFlag", "valid", "public",

                   #"boolean_crystallisation_outcome_manual_0"]
                   ]

unknown_tokens = {"?", ""}
train_percentage = 0.7
max_entries = None
filename = "test_data/DRP.csv"

def load_data():
  with open(filename) as f:
    reader = csv.reader(f)
    data = [row for row in reader]
    headers = data.pop(0)

    # Assign the appropriate types to each header.
    correct_types = {h:float for h in headers}
    for h in str_headers: correct_types[h] = str

    # Remove unhelpful headers from the dataset.
    ignored_indices = {headers.index(header) for header in ignored_headers}
    headers = [h for i,h in enumerate(headers) if i not in ignored_indices]
    data = [[e for i,e in enumerate(row) if i not in ignored_indices] for row in data]

    if max_entries:
      data = random.sample(data, max_entries)

    for i, row in enumerate(data):
      for j, header in enumerate(headers):
        correct_type = correct_types[header]
        data[i][j] = correct_type(row[j]) if row[j] not in unknown_tokens else 0.0

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


if __name__=="__main__":
  test()



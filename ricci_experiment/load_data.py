import random
import csv

def load_data():
  filename = "test_data/RicciDataMod.csv"
  with open(filename) as f:
    reader = csv.reader(f)
    data = [row for row in reader]
    headers = data.pop(0)
    train = data[:len(data)/2]
    test = data[:len(data)/2]
  return headers, train, test


def test():
  headers, train, test = load_data()
  print "load_data -- unpacks correctly? -- ", (headers != None and train != None and test != None)

if __name__=="__main__":
  test()



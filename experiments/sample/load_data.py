import random

def load_data():
  headers = ["Feature A (i)", "Feature B (2i)", "Feature C (-i)",
             "Random Feature", "Outcome"]
  train = [[i, 2*i, -i, random.random(), "A"] for i in range(0,100)] + \
          [[i, 2*i, -i, random.random(), "B"] for i in range(100,200)]
  test = [[i, 2*i, -i, random.random(), "A"] for i in range(0,100)] + \
          [[i, 2*i, -i, random.random(), "B"] for i in range(100,200)]
  return headers, train, test

#TODO: Adding a "Constant" feature with all values identical results in a not-very-good repair.

def test():
  headers, train, test = load_data()
  print "load_data -- unpacks correctly? -- ", (headers != None and train != None and test != None)

if __name__=="__main__":
  test()



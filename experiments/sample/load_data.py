import random

def load_data():
  N = 1000
  headers = ["Feature A (i)", "Feature B (2i)", "Feature C (-i)",
             "Constant Feature", "Random Feature", "Outcome"]
  train = [[i, 2*i, -i, 1, random.random(), "A"] for i in range(0,N)] + \
          [[i, 2*i, -i, 1, random.random(), "B"] for i in range(N,2*N)]
  test = [[i, 2*i, -i, 1, random.random(), "A"] for i in range(0,N)] + \
          [[i, 2*i, -i, 1, random.random(), "B"] for i in range(N,2*N)]
  return headers, train, test

def test():
  headers, train, test = load_data()
  print "load_data -- unpacks correctly? -- ", (headers != None and train != None and test != None)

if __name__=="__main__":
  test()



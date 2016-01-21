def load_data():
  headers = ["Feature A", "Feature B", "Feature C", "Outcome"]
  train = [[i, 2*i, -i, "A"] for i in range(0,100)] + \
          [[i, 2*i, -i, "B"] for i in range(1,200)]
  test = [[i, 2*i, -i, "A"] for i in range(0,100)] + \
          [[i, 2*i, -i, "B"] for i in range(1,200)]
  return headers, train, test


def test():
  headers, train, test = load_data()
  print "load_data -- unpacks correctly? -- ", (headers != None and train != None and test != None)

if __name__=="__main__":
  test()



def accuracy(conf_matrix):
  total, correct = 0.0, 0.0
  for true_response, guess_dict in conf_matrix.items():
    for guess, count in guess_dict.items():
      if true_response == guess:
        correct += count
      total += count
  return correct/total


def test():
  conf_matrix = {"A":{"A":10}, "B":{"A":5,"B":5}}

  print "measurements -- accuracy correct? -- ", accuracy(conf_matrix) == 0.75

if __name__=="__main__":
  test()

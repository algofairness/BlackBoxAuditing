def accuracy(conf_matrix):
  total, correct = 0.0, 0.0
  for true_response, guess_dict in conf_matrix.items():
    for guess, count in guess_dict.items():
      if true_response == guess:
        correct += count
      total += count
  return correct/total


def get_conf_matrix(prediction_tuples):
  # Produce a confusion matrix in a dictionary format from those predictions.
  conf_table = {}
  for actual, guess in prediction_tuples:
    guess = convert_to_type(actual, guess) # ... Since file-reading changes types.

    if not actual in conf_table:
      conf_table[actual] = {}

    if not guess in conf_table[actual]:
      conf_table[actual][guess] = 1
    else:
      conf_table[actual][guess] += 1

  return conf_table

def convert_to_type(actual, guess):
  if type(actual) == bool:
    guess = guess=="True"
  else:
    actual_type = type(actual)
    guess = actual_type(guess)
  return guess

def test():
  conf_matrix = {"A":{"A":10}, "B":{"A":5,"B":5}}
  print "measurements -- accuracy correct? -- ", accuracy(conf_matrix) == 0.75

  pred_tuples = [(1,1),(1,1),(2,2),(3,3),(1,3),(3,1)]
  correct_conf_matrix = {1:{1:2, 3:1}, 2:{2:1}, 3:{1:1, 3:1}}
  conf_matrix = get_conf_matrix(pred_tuples)
  print "confusion matrix correct? -- ", conf_matrix == correct_conf_matrix

if __name__=="__main__":
  test()

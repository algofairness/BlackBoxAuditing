import random

def accuracy(conf_matrix):
  total, correct = 0.0, 0.0
  for true_response, guess_dict in conf_matrix.items():
    for guess, count in guess_dict.items():
      if true_response == guess:
        correct += count
      total += count
  return correct/total

def precision(conf_matrix):
  return random.random() #TODO

def recall(conf_matrix):
  return random.random() #TODO



def test():
  pass

if __name__=="__main__":
  test()

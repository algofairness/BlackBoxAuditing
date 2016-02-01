
import random

def split_by_percent(data, train_percentage):
  train_indices = random.sample(range(len(data)), int(train_percentage*len(data)))
  train = [row for i,row in enumerate(data) if i in train_indices]
  test = [row for i,row in enumerate(data) if i not in train_indices]
  return train, test

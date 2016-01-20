from abc import ABCMeta, abstractmethod
import time

class AbstractModelFactory(object):
  __metaclass__ = ABCMeta

  def __init__(self, all_data, headers, response_header, name_prefix=""):
    self.all_data = all_data
    self.headers = headers
    self.response_header = response_header
    self.model_name = "{}_{}".format(name_prefix, time.time()) if name_prefix else time.time()

  @abstractmethod
  def build(self, train_set):
    pass

def test():
  pass

if __name__=="__main__":
  test()

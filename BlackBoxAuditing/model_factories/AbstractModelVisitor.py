from abc import ABCMeta, abstractmethod
import time

class AbstractModelVisitor(object, metaclass=ABCMeta):
  def __init__(self, model_name):
    self.model_name = "{}".format(time.time())

  @abstractmethod
  def test(self, test_set):
    pass

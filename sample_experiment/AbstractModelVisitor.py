from abc import ABCMeta, abstractmethod

class AbstractModelVisitor(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def test(self, test_set):
    pass

def test():
  pass

if __name__=="__main__":
  test()

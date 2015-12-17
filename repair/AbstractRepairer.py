from abc import ABCMeta, abstractmethod

class AbstractRepairer(object):
  """
  A Repairer object is capable of removing a pre-determined feature from
  a dataset at a specific `repair_level`.
  """

  __metaclass__ = ABCMeta

  def __init__(self, all_data, feature_to_repair, repair_level):
    self.all_data = all_data
    self.featute_to_repair = feature_to_repair
    self.repair_level = repair_level

  @abstractmethod
  def repair(data_to_repair):
    pass


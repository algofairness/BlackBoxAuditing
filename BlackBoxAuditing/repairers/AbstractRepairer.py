from abc import ABCMeta, abstractmethod

class AbstractRepairer(object, metaclass=ABCMeta):
  """
  A Repairer object is capable of removing the correlations of a feature
  from a dataset at a specific `repair_level`.
  """

  def __init__(self, all_data, feature_to_repair, repair_level, kdd, features_to_ignore=[], repair_mode="Orig", spec_group=None):
    """
    all_data should be a list of rows (ie, a list of lists) composing the entire
    test and training dataset. Headers should not be included in data sets.

    feature_to_repair should be the index of the feature to repair. (ie, 0 to k)
    where k is the number of features in the dataset.

    repair_level should be a float between [0,1] representing the level of repair.

    features_to_ignore should be a list of feature indexes that should be ignored.
    """

    self.all_data = all_data
    self.feature_to_repair = feature_to_repair
    self.repair_level = repair_level
    self.kdd = kdd
    self.features_to_ignore = features_to_ignore
    self.repair_mode = repair_mode
    self.spec_group = spec_group

  @abstractmethod
  def repair(self, data_to_repair):
    """
    data_to_repair is the list of rows that actually should be repaired.
    """
    pass

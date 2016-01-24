from AbstractRepairer import AbstractRepairer
from CategoricToNumericRepairer import Repairer as CTN_Repairer
from NumericToNumericRepairer import Repairer as NTN_Repairer

class Repairer(AbstractRepairer):
  def __init__(self, *args, **kwargs):
    super(Repairer, self).__init__(*args, **kwargs)

    if all(isinstance(row[self.feature_to_repair],float) for row in self.all_data):
      self.repairer = NTN_Repairer(*args, **kwargs)
    elif all(isinstance(row[self.feature_to_repair],int) for row in self.all_data):
      self.repairer = NTN_Repairer(*args, **kwargs)
    elif all(isinstance(row[self.feature_to_repair],str) for row in self.all_data):
      self.repairer = CTN_Repairer(*args, **kwargs)

  def repair(self, data_to_repair):
    return self.repairer.repair(data_to_repair)

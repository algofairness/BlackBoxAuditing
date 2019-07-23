from BlackBoxAuditing.repairers.AbstractRepairer import AbstractRepairer
from BlackBoxAuditing.repairers.CategoricRepairer import Repairer as CategoricRepairer
from BlackBoxAuditing.repairers.CategoricRepairerAllMedian import Repairer as CategoricRepairerAllMed
from BlackBoxAuditing.repairers.CategoricRepairerUniqueMedian import Repairer as CategoricRepairerUMed
from BlackBoxAuditing.repairers.CategoricRepairerMode import Repairer as CategoricRepairerMode
from BlackBoxAuditing.repairers.NumericRepairer import Repairer as NumericRepairer

class Repairer(AbstractRepairer):
  def __init__(self, *args, **kwargs):
    super(Repairer, self).__init__(*args, **kwargs)
    
    if self.kdd:
      if self.repair_mode == "AllMed":
        self.repairer = CategoricRepairerAllMed(*args,**kwargs)
      elif self.repair_mode == "UMed":
        self.repairer = CategoricRepairerUMed(*args,**kwargs)
      elif self.repair_mode == "Mode":
        self.repairer = CategoricRepairerMode(*args,**kwargs)
      else:
        self.repairer = CategoricRepairer(*args,**kwargs)
    else:
      if all(isinstance(row[self.feature_to_repair],float) for row in self.all_data):
        self.repairer = NumericRepairer(*args, **kwargs)
      elif all(isinstance(row[self.feature_to_repair],int) for row in self.all_data):
        self.repairer = NumericRepairer(*args, **kwargs)
      elif all(isinstance(row[self.feature_to_repair],str) for row in self.all_data):
        if self.repair_mode == "AllMed":
          self.repairer = CategoricRepairerAllMed(*args,**kwargs)
        elif self.repair_mode == "UMed":
          self.repairer = CategoricRepairerUMed(*args,**kwargs)
        elif self.repair_mode == "Mode":
          self.repairer = CategoricRepairerMode(*args,**kwargs)
        else:
          self.repairer = CategoricRepairer(*args,**kwargs)

  def repair(self, data_to_repair):
    return self.repairer.repair(data_to_repair)

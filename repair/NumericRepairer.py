from AbstractRepairer import AbstractRepairer
import CategoricRepairer
from binning.Binner import make_histogram_bins
from binning.BinSizes import FreedmanDiaconisBinSize as bin_calculator
from calculators import get_median

class Repairer(AbstractRepairer):
  def __init__(self, *args, **kwargs):
    super(Repairer, self).__init__(*args, **kwargs)
    self.categoric_repairer = CategoricRepairer.Repairer(*args, **kwargs)

  def repair(self, data_to_repair):

    # Convert the "feature_to_repair" into a pseudo-categorical feature by
    # applying binning on that column.
    binned_data_to_repair = [row[:] for row in data_to_repair]
    bins = make_histogram_bins(bin_calculator, data_to_repair, self.feature_to_repair)
    for i, binned_data in enumerate(bins):
      bin_name = "BIN_{}".format(i) # IE, the "category" to replace numeric values.
      for binned_row in binned_data:
        for j, row in enumerate(binned_data_to_repair):
          if row == binned_row: # TODO: This isn't the best way to do this...
            binned_data_to_repair[j][self.feature_to_repair] = bin_name

    repaired_data = self.categoric_repairer.repair(binned_data_to_repair)

    # Replace the "feature_to_repair" column with the median numeric value.
    median = get_median([row[self.feature_to_repair] for row in data_to_repair])
    for i in xrange(len(repaired_data)):
      if self.repair_level > 0:
        repaired_data[i][self.feature_to_repair] = median
      else:
        repaired_data[i][self.feature_to_repair] = data_to_repair[i][self.feature_to_repair]

    return repaired_data


def test():
  test_sample()

def test_sample():
  data = [[float(i),float(i)*2, 1] for i in xrange(0, 150)]
  feature_to_repair = 0
  repairer = Repairer(data, feature_to_repair, 0.5)
  repaired_data = repairer.repair(data)
  print "repaired_data altered?", repaired_data != data

  median = get_median([row[feature_to_repair] for row in data])
  print "median replaces column?", all(row[feature_to_repair] == median for row in repaired_data)

  repairer = Repairer(data, feature_to_repair, 0.0)
  repaired_data = repairer.repair(data)
  print "repaired_data unaltered for repair level=0?", repaired_data == data


if __name__=="__main__":
  test()


import numpy

def FreedmanDiaconisBinSize(feature_values):
  """
  The bin size in FD-binning is given by size = 2 * IQR(x) * n^(-1/3)
  More Info: https://en.wikipedia.org/wiki/Freedman%E2%80%93Diaconis_rule
  """

  q75, q25 = numpy.percentile(feature_values, [75 ,25])
  IQR = q75 - q25

  return 2 * IQR * len(feature_values)^(-1.0/3.0)

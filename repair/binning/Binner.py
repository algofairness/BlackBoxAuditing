def make_histogram_bins(bin_size_calculator, data, col_id):
  feature_vals = [row[col_id] for row in data]
  bin_size = bin_size_calculator(feature_vals)

  sorted_data = sorted(data, key=lambda row: row[col_id])

  num_bins = len(sorted_data)/bin_size
  bins = [sorted_data[bin_size*i:bin_size*(i+1)] for i in xrange(num_bins)]

  return bins


def test():
  data = [[i,0] for i in xrange(0, 100)]

  from BinSizes import FreedmanDiaconisBinSize as bsc
  bins = make_histogram_bins(bsc, data, 0)

  print "make_histogram_bins -- no features lost --", (len(bins[0]) == len(bins[-1]) == 21)

  print "make_histogram_bins -- correct # of bins --", (len(bins) == 4)




if __name__=="__main__":
  test()

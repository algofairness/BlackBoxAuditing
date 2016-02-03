import math

def make_histogram_bins(bin_size_calculator, data, col_id):
  feature_vals = [row[col_id] for row in data]
  bin_size = bin_size_calculator(feature_vals)

  # Round the number of buckets up so we don't lose any data.
  num_bins = int(math.ceil(len(data)/float(bin_size)))

  data_tuples = list(enumerate(data)) # [(0,row), (1,row'), (2,row''), ... ]
  sorted_data_tuples = sorted(data_tuples, key=lambda tup: tup[1][col_id])

  sorted_index = [i for i,_ in sorted_data_tuples]
  index_bins = [sorted_index[bin_size*i:bin_size*(i+1)] for i in xrange(num_bins)]

  return index_bins


def test():
  data = [[i,0] for i in xrange(0, 100)]

  from BinSizes import FreedmanDiaconisBinSize as bsc
  bins = make_histogram_bins(bsc, data, 0)
  print bins, len(bins), len(bins[0])

  print "make_histogram_bins -- no entries lost --", sum(len(row) for row in bins) == len(data)

  print "make_histogram_bins -- correct # of bins --", (len(bins) == 5)




if __name__=="__main__":
  test()

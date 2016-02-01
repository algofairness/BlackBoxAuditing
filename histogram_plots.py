import matplotlib.pyplot as plt


def graph_histogram(data, output_image_file):
  plt.hist(data)
  plt.savefig(output_image_file)


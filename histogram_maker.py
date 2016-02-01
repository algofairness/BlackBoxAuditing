# NOTE: These settings and imports should be the only things that change
#       across experiments on different datasets 

from experiments.arrests.load_data import load_data
from repair.CategoricRepairer import Repairer
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NOTE: You should not need to change anything below this point.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from histogram_plots import graph_histogram
#TODO: Get group level data to plot 
def run():
  feature_to_repair = 0
  repair_level = 1.0
  _, train_data, test_data = load_data()

  repairer = Repairer(train_data+test_data, feature_to_repair, repair_level)
  repaired_data = repairer.repair(test_data)

  output_image_file = "graph_histogram.png"
  graph_histogram(repaired_data[1], output_image_file)
 


if __name__=="__main__":
  run()

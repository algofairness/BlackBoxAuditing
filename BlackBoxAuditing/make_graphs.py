"""
Development script for converting audit files into graphs.
"""

from BlackBoxAuditing.audit_reading import graph_audits, graph_audit, rank_audit_files, graph_distributions
from BlackBoxAuditing.measurements import BCR, accuracy

from os import listdir
from os.path import isfile, join

import sys


def audit_directory(directory, response_header, write_to_file=True, print_all_data=False, dump_all=False, conf_matrices_for_all_features=None, test_data=None, all_repaired_data=None, headers=None):
  # Ensures that if write_to_file is False, the necessary data is given
  if not write_to_file and (conf_matrices_for_all_features == None or test_data == None or all_repaired_data == None or headers == None):
    raise Exception("if write_to_file is False, additional data must be provided")
    
  measurers = [accuracy, BCR]
  if write_to_file:
    # gets the audit files to graph
    only_files = [f for f in listdir(directory) if isfile(join(directory, f))]
    audits = ["{}/{}".format(directory, f) for f in only_files if f[-6:]==".audit"]

    #graphs each audit file
    for audit in audits:
      audit_image_filename = audit + ".png"
      graph_audit(audit, measurers, audit_image_filename)

    #graphs each measure
    for measurer in measurers:
      ranked_graph_filename = "{}/{}.png".format(directory, measurer.__name__)
      graph_audits(audits, measurer, ranked_graph_filename)
      ranks = rank_audit_files(audits, measurer)
      print(measurer.__name__, ranks)

    #graphs each distribution
    for file_name in only_files:
      for g in list(range(0, 10)):
        if "{}.data".format(g) in file_name:
          graph_distributions(directory, file_name, response_header)
  else:
    #graphs each audit file and measure
    for i, feature in enumerate(conf_matrices_for_all_features):
      graph_audit(None, measurers, None, write_to_file=write_to_file, print_all_data=print_all_data, feature=feature, confusion_matrices=conf_matrices_for_all_features[feature])

    #graphs each distribution
    for feature in all_repaired_data:
      rfi = headers.index(feature)
      if not dump_all:
        graph_distributions(None, None, response_header, write_to_file=write_to_file, rep_feat_index=rfi, test_data=test_data, repaired_data=all_repaired_data[feature][1.0], headers=headers)
      else:
        for rep_lev in sorted(all_repaired_data[feature].keys()):
          graph_distributions(None, None, response_header, write_to_file=write_to_file, rep_feat_index=rfi, test_data=test_data, repaired_data=all_repaired_data[feature][rep_lev], headers=headers, rep_lev=rep_lev)

def graph_particular_distribution(directory, file, response_header, num_feat_index, only_groups=None):
  repair_level = (file.split("_")[1]).split(".")[0] + "." + (file.split("_")[1]).split(".")[1]
  graph_distributions(directory, file, response_header, rep_lev=repair_level, particular=True, num_feat_index=num_feat_index, only_groups=only_groups)


if __name__=="__main__":
  try:
    directory = sys.argv[1]
    audit_directory(directory)
  except:
    print("proper usage: make_graphs.py <directory/with/audits>")




from repair.GeneralRepairer import Repairer
from loggers import vprint
import csv
import time
import os
import json

class GradientFeatureAuditor(object):
  def __init__(self, model, headers, train_set, test_set, repair_steps=10,
                features_to_ignore = []):
    self.repair_steps = repair_steps
    self.model = model
    self.train_set = train_set
    self.test_set = test_set
    self.headers = headers
    self.features_to_ignore = features_to_ignore
    self.AUDIT_DIR = "audits"
    self.OUTPUT_DIR = "{}/{}".format(self.AUDIT_DIR, time.time())

    # Create any output directories that don't exist.
    for directory in [self.AUDIT_DIR, self.OUTPUT_DIR]:
      if not os.path.exists(directory):
        os.makedirs(directory)


  def audit_feature(self, feature_to_repair, output_file, save_repaired_data=True):
    conf_tables = []
    repair_increase_per_step = 1.0/self.repair_steps
    repair_level = 0.0

    while repair_level <= 1.0:
      all_data = self.train_set + self.test_set
      index_to_repair = self.headers.index(feature_to_repair)
      repairer = Repairer(all_data, index_to_repair, repair_level,
                          features_to_ignore=self.features_to_ignore)
      rep_test = repairer.repair(self.test_set)

      if save_repaired_data:
        with open(output_file + ".repaired_{}.data".format(repair_level), "w") as f:
          writer = csv.writer(f)
          for row in [self.headers]+rep_test:
            writer.writerow(row)

      conf_table = self.model.test(rep_test)

      conf_tables.append( (repair_level, conf_table) )
      repair_level += repair_increase_per_step

    with open(output_file, "a") as f:
      f.write("GFA Audit for:{}\n".format(feature_to_repair))
      for repair_level, conf_table in conf_tables:
        json_conf_table = json.dumps(conf_table)
        f.write("{}:{}\n".format(repair_level, json_conf_table))

  def audit(self, verbose=False):
    output_files = []

    features_to_audit = [h for i, h in enumerate(self.headers) if i not in self.features_to_ignore]
    for i, feature in enumerate(features_to_audit):
      message = "Auditing: '{}' ({}/{}).".format(feature,i+1,len(features_to_audit))
      vprint(message, verbose)

      cleaned_feature_name = feature.replace(".","_").replace(" ","_")
      output_file = "{}.audit".format(cleaned_feature_name)
      full_filepath = self.OUTPUT_DIR + "/" + output_file
      self.audit_feature(feature, full_filepath)
      output_files.append(full_filepath)

    print "Audit files dumped to: {}".format(self.OUTPUT_DIR)

    return output_files


def test():
  class MockModel(object):
    def test(self, test_set, response_col=0):
      conf_table = {}
      for entry in test_set:
        actual = entry[response_col]
        guess = actual

        if not actual in conf_table:
          conf_table[actual] = {}

        if not guess in conf_table[actual]:
          conf_table[actual][guess] = 1
        else:
          conf_table[actual][guess] += 1
      return conf_table

  model = MockModel()
  headers = ["response", "duplicate", "constant"]
  train = [[i,i,1] for i in xrange(100)]
  test = train[:] # Copy the training data.
  repair_steps = 5
  gfa = GradientFeatureAuditor(model, headers, train, test, repair_steps=repair_steps)
  output_files = gfa.audit()

  print "correct # of audit files produced? --", len(output_files) == len(train[0]) # The number of features.


  with open(output_files[0]) as f:
    print "correct # of lines per file? --", len(f.readlines()) == repair_steps+2 # +1 for the header-line and +1 for the level=0 step.

  files_not_empty = all(os.stat(f).st_size!=0 for f in output_files)
  print "all audit files not empty? --", files_not_empty

if __name__=="__main__":
  test()

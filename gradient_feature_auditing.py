from repair.GeneralRepairer import Repairer #TODO: Build the GeneralRepairer...
import time
import os

class GradientFeatureAuditor(object):
  def __init__(self, model, headers, train_set, test_set, repair_steps=10):
    self.repair_steps = repair_steps
    self.model = model
    self.train_set = train_set
    self.test_set = test_set
    self.headers = headers
    self.OUTPUT_DIR = "audits"

  def audit_feature(self, feature_to_repair, output_file):
    conf_tables = []
    repair_increase_per_step = 1.0/self.repair_steps
    repair_level = 0.0

    while repair_level <= 1.0:
      all_data = self.train_set + self.test_set
      repairer = Repairer(all_data, feature_to_repair, repair_level)
      rep_test = repairer.repair(self.test_set)

      conf_table = self.model.test(rep_test)

      conf_tables.append( (repair_level, conf_table) )
      repair_level += repair_increase_per_step

    with open(output_file, "a") as f:
      f.write("GFA Audit for: {}\n".format(feature_to_repair))
      for repair_level, conf_table in conf_tables:
        f.write("{}:{}\n".format(repair_level, conf_table))

  def audit(self):
    output_files = []

    for feature in self.headers:
      cleaned_feature_name = feature.replace(".","_").replace(" ","_")
      output_file = "{}_{}.audit".format(cleaned_feature_name, time.time())
      full_filepath = self.OUTPUT_DIR + "/" + output_file
      self.audit_feature(feature, full_filepath)
      output_files.append(full_filepath)

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

  print "GradientFeatureAuditor -- correct # of audit files produced? --", len(output_files) == len(train[0]) # The number of features.


  with open(output_files[0]) as f:
    print "GradientFeatureAuditor -- correct # of lines per file? --", len(f.readlines()) == repair_steps+2 # +1 for the header-line and +1 for the level=0 step.

  files_not_empty = all(os.stat(f).st_size!=0 for f in output_files)
  print "GradientFeatureAuditor -- all audit files not empty? --", files_not_empty

if __name__=="__main__":
  test()

from repair.GeneralRepairer import Repairer
import time

class GradientFeatureAuditor(object):
  def __init__(self, model, headers, train_set, test_set, repair_step=10):
    self.repair_step = repair_step
    self.model = model
    self.train_set = train_set
    self.test_set = test_set
    self.headers = headers
    self.OUTPUT_DIR = "audits"

  def audit_feature(self, feature_to_repair, output_file):
    conf_tables = []

    for repair_level in xrange(0,101,self.repair_step):
      all_data = [self.headers] + self.train_set + self.test_set
      repairer = Repairer(all_data, feature_to_repair, repair_level)
      rep_test = repairer.repair(self.test_set)

      conf_table = self.model.test(rep_test)

      conf_tables.append( (repair_level, conf_table) )

    with open(output_file, "a") as f:
      f.write("GFA Audit for \"{}\"\n".format(feature_to_repair))
      for repair_level, conf_table in conf_tables:
        f.write("{}:{}\n".format(repair_level, conf_table))

  def audit(self):
    output_files = []

    for feature in self.headers:
      output_file = "{}/{}_{}.audit".format(self.OUTPUT_DIR, feature, time.time())
      self.audit_feature(feature, output_file)
      output_files.append(output_file)

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
  gfa = GradientFeatureAuditor(model, headers, train, test)
  output_files = gfa.audit()

  import os
  files_not_empty = all(os.stat(f).st_size!=0 for f in output_files)

  print "GradientFeatureAuditor pass?", files_not_empty

if __name__=="__main__":
  test()

from repair.GeneralRepairer import Repairer
import time

class GradientFeatureAuditor(object):
  def __init__(self, model, headers, train_set, test_set, repair_steps=10):
    self.repair_steps = repair_steps
    self.model = model
    self.train_set = train_set
    self.test_set = test_set
    self.headers = headers

  def audit_feature(self, feature_to_repair, output_file):
    conf_tables = []

    for repair_level in xrange(0,101,self.repair_steps):
      all_data = [self.headers] + self.train_set + self.test_set
      repairer = Repairer(all_data, feature_to_repair, repair_level)
      rep_test = repairer.obfuscate(self.test_set)

      conf_table = self.model.test(rep_test)

      conf_tables.append( (repair_level, conf_table) )

    with open(output_file, "a") as f:
      f.write("{}: {}\n".format(feature_to_repair, conf_tables))

  def audit(self):
    for feature in self.headers:
      output_file = "{}_{}.dump".format(feature, time.time())
      self.audit_feature(feature, output_file)

class Obfuscator(object):
  def __init__(self, all_data, feature_to_remove, portion_to_remove):
    self.all_data = all_data
    self.featute_to_remove = feature_to_remove
    self.portion_to_remove = portion_to_remove

  def obfuscate(data_to_obfuscate):
    pass #TODO: Import le magic.


class Auditor(object):
  def __init__(self, model_factory, headers, train_set, test_set):
    self.PORTION_STEP = 10
    self.model_factory = model_factory
    self.train_set = train_set
    self.test_set = test_set
    self.headers = headers

  def audit(self, feature_to_remove, output_file, train_obf_models=False):
    conf_tables = []

    orig_model = self.model_factory.build(self.train_set)

    for portion_to_remove in xrange(0,101,self.PORTION_STEP):
      all_data = [self.headers] + self.train_set + self.test_set
      obfuscator = Obfuscator(all_data, feature_to_remove, portion_to_remove)
      obf_test = obfuscator.obfuscate(self.test_set)

      if train_obf_models:
        obf_train = obfuscator.obfuscate(self.train_set)
        obf_model = self.model_factory.build(obf_train)
        conf_table = obf_model.test(obf_test)

      else:
        conf_table = orig_model.test(obf_test)

      conf_tables.append( (portion_to_remove, conf_table) )

    with open(output_file, "a") as f:
      f.write("{}: {}\n".format(feature_to_remove, conf_tables))



from AbstractModelFactory import AbstractModelFactory
from AbstractModelVisitor import AbstractModelVisitor
import time

class ModelFactory(AbstractModelFactory):

  def build(self, train_set):
    arff_types = get_arff_type_dict(self.headers, self.all_data)
    train_arff = list_to_arff_file(arff_types, train_set)
    model_file = "SVM_{}.model".format(self.model_name)

    command = "Build me a model using {}".format(train_arff) #TODO: Make this right.
    run_weka_command(command)

    return ModelVisitor(model_file, arff_types)



class ModelVisitor(AbstractModelVisitor):

  def __init__(self, model_file, arff_types):
    self.model_file = model_file
    self.arff_types = arff_types
    self.model_tag = time.time()

  def test(self, test_set):
    #TODO: Spit out a conf-matrix using Le WEKA.
    pass


def run_weka_command(command):
  #TODO: Run Weka command after setting the classpath.
  pass


def get_arff_type_dict(headers, data):
  values = {header:[row[i] for row in data] for i, header in enumerate(headers)}
  arff_type = {}
  for header in headers:
    if all( map(lambda x: isinstance(x, float), values[header]) ):
      arff_type[header] = "NUMERIC"
    elif all( map(lambda x: isinstance(x, int), values[header]) ):
      arff_type[header] = "NUMERIC"
    else:
      arff_type[header] = values[header] # Categorical
  return arff_type


def list_to_arff_file(arff_type_dict, data):
  #TODO: Write the arff to the system.
  pass


def test():
  headers = ["predictor", "response"]
  train_set = [[float(i), "A"] for i in xrange(1,100)]
  test_set = [[float(i), "B"] for i in xrange(101,200)]
  all_data = train_set + test_set

  factory = ModelFactory(all_data, headers, "response", name_prefix="test")
  model = factory.build(train_set)

  print "SVMModelFactory -- factory builds ModelVisitor? -- ", isinstance(model, ModelVisitor)

if __name__=="__main__":
  test()

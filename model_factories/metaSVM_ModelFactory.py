from AbstractWekaModelFactory import AbstractWekaModelFactory, AbstractWekaModelVisitor

class ModelFactory(AbstractWekaModelFactory):

  def __init__(self, *args, **kwargs):

    # Use the specified kernel if specified, or else use WEKA's default.
    self.kernel = ""
    if "options" in kwargs:
      options = kwargs["options"]
      if "kernel" in options:
        self.kernel = options.pop("kernel")

    super(ModelFactory, self).__init__(*args,**kwargs)

    self.model_visitor_type = ModelVisitor
    self.verbose_factory_name = "Support_Vector_Machine"

    all_data = self.all_data
    total = float(len(all_data))
    class0 = 0
    class1 = 0
    for point in all_data:
      if point[0] == "0":
        class0 += 1
      elif point[0] == "1":
        class1 += 1
      else:
        print "ERROR"
    p0 = class0/total
    print p0
    p1 = class1/total
    print p1
    cost_matrix = "\"[0.0 {}; {} 0.0]\"".format(p0,p1)
    command = "weka.classifiers.meta.CostSensitiveClassifier -cost-matrix {} -W weka.classifiers.functions.SMO".format(cost_matrix)

    # If a kernel option is listed, include it in the command.
    if self.kernel:
      command += " -K \"{}\"".format(self.kernel)

    self.train_command = command

class ModelVisitor(AbstractWekaModelVisitor):
  def __init__(self, *args, **kwargs):
    super(ModelVisitor, self).__init__(*args,**kwargs)
    self.test_command = "weka.classifiers.functions.SMO"


def test():
  headers = ["predictor", "response"]
  A_set = [[i, "A"] for i in range(1,50)]
  B_set = [[i, "B"] for i in range(51,100)]
  C_set = [[i, "C"] for i in range(51,100)]
  train_set = A_set + B_set
  # Purposefully replace "B" with "C" in the test-set so that we *should* fail them.
  test_set = A_set + C_set
  all_data = train_set + test_set

  factory = ModelFactory(all_data, headers, "response", name_prefix="test")
  model = factory.build(train_set)
  print "factory builds ModelVisitor? -- ", isinstance(model, ModelVisitor)

  predictions = model.test(test_set)
  intended_predictions = [("A", "A")]*len(A_set) + [("C", "B")]*len(C_set)
  print "predicting correctly? -- ", predictions == intended_predictions

if __name__=="__main__":
  test()

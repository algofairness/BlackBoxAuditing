from AbstractWekaModelFactory import AbstractWekaModelFactory, AbstractWekaModelVisitor

class ModelFactory(AbstractWekaModelFactory):

  def __init__(self, *args, **kwargs):
    super(ModelFactory, self).__init__(*args,**kwargs)
    self.model_visitor_type = ModelVisitor
    self.verbose_factory_name = "Support_Vector_Machine"

    #self.kernel = "" # Weka defaults to a traditional linear classifier.
    self.kernel = "weka.classifiers.functions.supportVector.Puk -O 0.5 -S 7"
    command = "weka.classifiers.functions.SMO"

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

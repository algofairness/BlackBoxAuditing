from AbstractWekaModelFactory import AbstractWekaModelFactory, AbstractWekaModelVisitor

class ModelFactory(AbstractWekaModelFactory):

  def __init__(self, *args, **kwargs):
    super(ModelFactory, self).__init__(*args,**kwargs)
    self.model_visitor_type = ModelVisitor

    self.verbose_factory_name = "J48_Decision_Tree"
    self.train_command = "weka.classifiers.trees.J48"

class ModelVisitor(AbstractWekaModelVisitor):
  def __init__(self, *args, **kwargs):
    super(ModelVisitor, self).__init__(*args,**kwargs)
    self.test_command = "weka.classifiers.trees.J48"


def test():
  headers = ["predictor", "response"]
  train_set = [[i, "A"] for i in range(1,50)] + [[i, "B"] for i in range(51,100)]
  # Purposefully replace "B" with "C" so that we *should* fail them.
  test_set = [[i, "A"] for i in range(1,50)] + [[i, "C"] for i in range(51,100)]
  all_data = train_set + test_set

  factory = ModelFactory(all_data, headers, "response", name_prefix="test")
  model = factory.build(train_set)
  print "factory builds ModelVisitor? -- ", isinstance(model, ModelVisitor)

  predictions = model.test(test_set)
  intended_predictions = {'A': {'A': 49}, 'C': {'B': 49}}
  print "predicting correctly? -- ", predictions == intended_predictions

if __name__=="__main__":
  test()

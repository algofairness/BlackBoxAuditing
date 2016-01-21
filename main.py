
# NOTE: These settings and imports should be the only things that change
#       across experiments on different datasets and ML model types.
from sample_experiment.load_data import load_data
from sample_experiment.SVMModelFactory import ModelFactory
response_header = "Outcome"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NOTE: You should not need to change anything below this point.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def run():
  headers, train_set, test_set = load_data()

  """
   ModelFactories require a `build` method that accepts some training data
   with which to train a brand new model. This `build` method should output
   a Model object that has a `test` method -- which, when given test data
   in the same format as the training data, yields a confusion table detailing
   the correct and incorrect predictions of the model.
  """
  all_data = train_set + test_set
  model_factory = ModelFactory(all_data, headers, response_header)
  model = model_factory.build(train_set)

  from gradient_feature_auditing import GradientFeatureAuditor
  auditor = GradientFeatureAuditor(model, headers, train_set, test_set)
  auditor.audit()

if __name__=="__main__":
  run()

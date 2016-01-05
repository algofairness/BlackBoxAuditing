# CAUTION: THIS IS MEANT AS A GUIDELINE AND WILL NOT WORK AT THE MOMENT.

from DRP.load_data import load_data
from DRP.ModelFactory import ModelFactory

headers, train_set, test_set = load_data() #TODO: Implement this.

"""
 ModelFactories require a `build` method that accepts some training data
 with which to train a brand new model. This `build` method should output
 a Model object that has a `test` method -- which, when given test data
 in the same format as the training data, yields a confusion table detailing
 the correct and incorrect predictions of the model.
"""
model_factory = ModelFactory() # TODO: Implement this.
model = model_factory.build()

from gradient_feature_auditing import GradientFeatureAuditor
auditor = GradientFeatureAuditor(model, headers, train_set, test_set)
auditor.audit()


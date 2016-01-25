
# NOTE: These settings and imports should be the only things that change
#       across experiments on different datasets and ML model types.
from sample_experiment.load_data import load_data
from sample_experiment.SVMModelFactory import ModelFactory
from measurements import accuracy
response_header = "Outcome"
graph_measurements = [accuracy]
rank_measurement = accuracy
features_to_ignore = []

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NOTE: You should not need to change anything below this point.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from gradient_feature_auditing import GradientFeatureAuditor
from audit_reading import graph_audit, rank_audit_files

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

  # Don't audit the response feature.
  features_to_ignore.append(response_header)

  # Perform the Gradient Feature Audit and dump the audit results into files.
  auditor = GradientFeatureAuditor(model, headers, train_set, test_set,
                                   features_to_ignore=features_to_ignore)
  audit_filenames = auditor.audit()

  # Graph the audit files.
  for audit_filename in audit_filenames:
    audit_image_filename = audit_filename + ".png"
    graph_audit(audit_filename, graph_measurements, audit_image_filename)

  ranked_features = rank_audit_files(audit_filenames, rank_measurement)
  print ranked_features

if __name__=="__main__":
  run()

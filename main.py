# NOTE: These settings and imports should be the only things that change
#       across experiments on different datasets and ML model types.
from experiments.sample.load_data import load_data
from model_factories.SVM_ModelFactory import ModelFactory
from measurements import accuracy
response_header = "Outcome"
graph_measurers = [accuracy]
rank_measurer = accuracy
features_to_ignore = []

verbose = True # Set to `True` to allow for more detailed status updates.
save_repaired_data = True # Set to `True` to allow repaired data to be saved.
save_predictions_details = True # Set to `True` to save per-entry prediction info.

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NOTE: You should not need to change anything below this point.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from loggers import vprint
from GradientFeatureAuditor import GradientFeatureAuditor
from audit_reading import graph_audit, graph_audits, rank_audit_files
from measurements import get_conf_matrix

def run():
  headers, train_set, test_set = load_data()

  """
   ModelFactories require a `build` method that accepts some training data
   with which to train a brand new model. This `build` method should output
   a Model object that has a `test` method -- which, when given test data
   in the same format as the training data, yields a confusion table detailing
   the correct and incorrect predictions of the model.
  """

  vprint("Training initial model.",verbose)
  all_data = train_set + test_set
  model_factory = ModelFactory(all_data, headers, response_header)
  model = model_factory.build(train_set)

  # Check the quality of the initial model on verbose runs.
  if verbose:
    pred_tuples = model.test(train_set)
    conf_matrix = get_conf_matrix(pred_tuples)
    for measurer in graph_measurers:
      print "\t{}: {}".format(measurer.__name__, measurer(conf_matrix))

  # Don't audit the response feature.
  features_to_ignore.append(response_header)

  # Translate the headers into indexes for the auditor.
  feature_indexes_to_ignore = [headers.index(f) for f in features_to_ignore]

  # Perform the Gradient Feature Audit and dump the audit results into files.
  auditor = GradientFeatureAuditor(model, headers, train_set, test_set,
                                   features_to_ignore=feature_indexes_to_ignore,
                                   save_repaired_data=save_repaired_data,
                                   save_prediction_details=save_predictions_details)
  audit_filenames = auditor.audit(verbose=verbose)

  # Graph the audit files.
  vprint("Graphing audit files.",verbose)
  for audit_filename in audit_filenames:
    audit_image_filename = audit_filename + ".png"
    graph_audit(audit_filename, graph_measurers, audit_image_filename)

  ranked_graph_filename = "{}/{}.png".format(auditor.OUTPUT_DIR, rank_measurer.__name__)
  graph_audits(audit_filenames, rank_measurer, ranked_graph_filename)

  vprint("Ranking audit files.",verbose)
  ranked_features = rank_audit_files(audit_filenames, rank_measurer)
  print ranked_features


if __name__=="__main__":
  run()

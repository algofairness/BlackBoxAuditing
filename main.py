# NOTE: These settings and imports should be the only things that change
#       across experiments on different datasets and ML model types.
import experiments.sample as experiment
from model_factories.SVM_ModelFactory import ModelFactory
from measurements import accuracy, complement_BER
response_header = "Outcome"
graph_measurers = [accuracy, complement_BER]
rank_measurers = [accuracy, complement_BER]
features_to_ignore = []

verbose = True # Set to `True` to allow for more detailed status updates.
REPAIR_STEPS = 10
RETRAIN_MODEL_PER_REPAIR = False

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# NOTE: You should not need to change anything below this point.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from loggers import vprint
from GradientFeatureAuditor import GradientFeatureAuditor
from audit_reading import graph_audit, graph_audits, rank_audit_files, group_audit_ranks
from measurements import get_conf_matrix
from datetime import datetime
import csv

def run():

  start_time = datetime.now()

  headers, train_set, test_set = experiment.load_data()

  """
   ModelFactories require a `build` method that accepts some training data
   with which to train a brand new model. This `build` method should output
   a Model object that has a `test` method -- which, when given test data
   in the same format as the training data, yields a confusion table detailing
   the correct and incorrect predictions of the model.
  """

  all_data = train_set + test_set
  model_factory = ModelFactory(all_data, headers, response_header,
                               features_to_ignore=features_to_ignore)

  if not RETRAIN_MODEL_PER_REPAIR:
    vprint("Training initial model.",verbose)
    model = model_factory.build(train_set)

    # Check the quality of the initial model on verbose runs.
    if verbose:
      print "Calculating original model statistics on test data:"
      pred_tuples = model.test(test_set)
      conf_matrix = get_conf_matrix(pred_tuples)
      for measurer in graph_measurers:
        print "\t{}: {}".format(measurer.__name__, measurer(conf_matrix))
    model_or_factory = model
  else:
    model_or_factory = model_factory

  # Translate the headers into indexes for the auditor.
  audit_indices_to_ignore = [headers.index(f) for f in features_to_ignore]

  # Don't audit the response feature.
  audit_indices_to_ignore.append(headers.index(response_header))

  # Prepare the auditor.
  auditor = GradientFeatureAuditor(model_or_factory, headers, train_set, test_set,
                                   repair_steps=REPAIR_STEPS,
                                   features_to_ignore=audit_indices_to_ignore)

  vprint("Dumping original training data.", verbose)
  # Dump the train data to the log.
  train_dump = "{}/original_train_data.csv".format(auditor.OUTPUT_DIR)
  with open(train_dump, "w") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for row in train_set:
      writer.writerow(row)

  vprint("Dumping original testing data.", verbose)
  # Dump the train data to the log.
  test_dump = "{}/original_test_data.csv".format(auditor.OUTPUT_DIR)
  with open(test_dump, "w") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for row in test_set:
      writer.writerow(row)

  # Perform the Gradient Feature Audit and dump the audit results into files.
  audit_filenames = auditor.audit(verbose=verbose)

  # Graph the audit files.
  vprint("Graphing audit files.",verbose)
  for audit_filename in audit_filenames:
    audit_image_filename = audit_filename + ".png"
    graph_audit(audit_filename, graph_measurers, audit_image_filename)

  ranked_features = []
  for rank_measurer in rank_measurers:
    vprint("Ranking audit files by {}.".format(rank_measurer.__name__),verbose)
    ranked_graph_filename = "{}/{}.png".format(auditor.OUTPUT_DIR, rank_measurer.__name__)
    graph_audits(audit_filenames, rank_measurer, ranked_graph_filename)
    ranks = rank_audit_files(audit_filenames, rank_measurer)
    vprint("Ranked Features: {}".format(ranks), verbose)
    ranked_features.append( (rank_measurer, ranks) )

  end_time = datetime.now()

  # Store a summary of this experiment.
  summary_file = "{}/summary.txt".format(auditor.OUTPUT_DIR)
  with open(summary_file, "w") as f:
    f.write("Experiment Location: {}\n".format(experiment.__file__))
    f.write("Audit Start Time: {}\n".format(start_time))
    f.write("Audit End Time: {}\n".format(end_time))
    f.write("Retrained Per Repair: {}\n".format(RETRAIN_MODEL_PER_REPAIR))
    f.write("Model Factory ID: {}\n".format(model_factory.factory_name))
    f.write("Model Type: {}\n".format(model_factory.verbose_factory_name))
    f.write("Train Size: {}\n".format(len(train_set)))
    f.write("Test Size: {}\n".format(len(test_set)))
    f.write("Features: {}\n".format(headers))

    for ranker, ranks in ranked_features:
      f.write("Ranked Features by {}: {}\n".format(ranker.__name__, ranks))
      groups = group_audit_ranks(audit_filenames, ranker)
      f.write("  Approx. Trend Groups: {}\n".format(groups))

  vprint("Summary file written to: {}".format(summary_file), verbose)


if __name__=="__main__":
  run()

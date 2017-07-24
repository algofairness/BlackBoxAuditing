import argparse
import time
import os
from BlackBoxAuditing.find_contexts.convert_and_merge_files import convert_to_tab, merge
from BlackBoxAuditing.find_contexts.extract_influence_scores import extract_feature_influences
from BlackBoxAuditing.find_contexts.find_cn2_rules import CN2_learner
from BlackBoxAuditing.find_contexts.expand_and_find_contexts import expand_and_find_contexts


def context_finder(original_train_csv, original_test_csv, obscured_test_csv, output, summary_file, feature_data_file, removed_attr, beam_width, min_covered_examples, by_original, epsilon):
  # Create directory to dump results
  output_dir = output 

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  # Parse summary file for influence scores and generate obscured tag
  influence_scores, obscured_tag = extract_feature_influences(summary_file, removed_attr)

  # Convert original csv file to tab-separated
  # and create a new tab-separated file by merging original and obscured files
  original_train_tab = convert_to_tab(original_train_csv, feature_data_file, output_dir)
  original_test_tab = convert_to_tab(original_test_csv, feature_data_file, output_dir)
  merged_csv = merge(original_test_csv, obscured_test_csv, obscured_tag, output_dir)

  # Generate rule list for the original data using the CN2 algorithm
  rulesfile, accuracy, AUC = CN2_learner(original_train_tab, original_test_tab, output_dir, beam_width, min_covered_examples, max_rule_length, influence_scores)

  # Generate fully expanded rule list, store best expanded rule for each of the original rules,
  # and return contexts of discrimination
  contexts_of_influence = expand_and_find_contexts(original_test_csv, obscured_test_csv, merged_csv, rulesfile, influence_scores, obscured_tag, output_dir, by_original, epsilon)

  # Write results to summary file:
  summary = "{}/summary.txt".format(output_dir)
  summary_file = open(summary, 'w')

  summary_file.write("CN2 Settings Used:\n")
  summary_file.write("rules found for {}\n".format(original_train_csv))
  summary_file.write("beam_width: {}\n".format(beam_width))
  summary_file.write("min_covered_examples: {}\n".format(min_covered_examples))
  summary_file.write("max_rule_length: {}\n\n".format(max_rule_length))

  summary_file.write("CN2 Model Evaluation:\n")
  summary_file.write("Model tested on {}\n".format(original_test_csv))
  summary_file.write("Accuracy: {}\n".format(accuracy))
  summary_file.write("AUC: {}\n\n".format(AUC))

  summary_file.write("Contexts of influence found:\n")
  for outcome in contexts_of_influence:
    list_of_contexts = contexts_of_influence[outcome]
    contexts = " OR \n".join([" AND ".join(context) for context in list_of_contexts])
    summary_file.write(outcome +': \n')
    summary_file.write(contexts + '\n\n')

print("Summary of Experiment written to {}".format(summary))


import argparse
import time
import os
from find_contexts.find_cn2_rules import CN2_learner
from find_contexts.expand_and_find_contexts import expand_and_find_contexts


def context_finder(orig_train, orig_test, obscured_test, orig_train_tab, orig_test_tab, merged_data, output_dir, influence_scores, beam_width, min_covered_examples, max_rule_length, by_original, epsilon):
  # Generate rule list for the original data using the CN2 algorithm
  rulesfile, accuracy, AUC = CN2_learner(orig_train_tab, orig_test_tab, output_dir, beam_width, min_covered_examples, max_rule_length, influence_scores)

  # Generate fully expanded rule list, store best expanded rule for each of the original rules,
  # and return contexts of discrimination
  contexts_of_influence = expand_and_find_contexts(orig_test, obscured_test, merged_data, rulesfile, influence_scores, obscured_tag, output_dir, by_original, epsilon)

  parsed_contexts = []
  for outcome in contexts_of_influence:
    list_of_contexts = contexts_of_influence[outcome]
    contexts = " OR \n".join([" AND ".join(context) for context in list_of_contexts])
    parsed_contexts.append((outcome, contexts))
    summary_file.write(outcome +': \n')
    summary_file.write(contexts + '\n\n')

  # Store summary results:
  summary_info = ["CN2 Settings Used:",
                  "rules found for {}".format(original_train_csv),
                  "beam_width: {}".format(beam_width),
                  "min_covered_examples: {}".format(min_covered_examples),
                  "max_rule_length: {}\n".format(max_rule_length),
                  "CN2 Model Evaluation:",
                  "Model tested on {}".format(original_test_csv),
                  "Accuracy: {}".format(accuracy),
                  "AUC: {}\n".format(AUC)]

  # Print summary results
  for info_line in summary_info:
    print(summary_info)

   
  print("Contexts of influence found:")
  for parsed_context in parsed_contexts:
    print(parsed_context[0])
    print(parsed_context[1])

    
  # Write results to summary file:
  summary = "{}/summary.txt".format(output_dir)
  summary_file = open(summary, 'w')

  for info_line in summary_info:
    summary_file.write(info_line+'\n')

  summary_file.write("Contexts of influence found:\n")
  for parsed_context in parsed_contexts:
    summary_file.write(parsed_context[0]+':\n')
    summary_file.write(parsed_context[1]+'\n\n')

  print("Summary of Experiment written to {}".format(summary))

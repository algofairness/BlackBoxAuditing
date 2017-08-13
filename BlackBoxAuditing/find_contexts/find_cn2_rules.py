import Orange
import os,csv

def CN2_learner(trainfile, testfile, output_dir, beam_width, min_covered_examples, max_rule_length, influence_scores):
  print("Setting up CN2 Learner")
  # format data for classification
  training_data = Orange.data.Table.from_file(trainfile)
  # set the learner
  learner = Orange.classification.rules.CN2Learner()
  # set the rule evaluator to be Laplace
  LaplaceEvaluator = Orange.classification.rules.LaplaceAccuracyEvaluator()
  learner.rule_finder.quality_evaluator = LaplaceEvaluator
  # set the number of solution steams considered at one time
  learner.rule_finder.search_algorithm.beam_width = beam_width
  # continuous value space is constrained to reduce computation time
  learner.rule_finder.search_strategy.constrain_continuous = True
  # set the minimum number of examples a found rule must cover to be considered
  learner.rule_finder.general_validator.min_covered_examples = min_covered_examples
  # set the maximum number of selectors (conditions) found rules may combine
  learner.rule_finder.general_validator.max_rule_length = max_rule_length

  print(("Learning rule list for {}".format(trainfile)))
  # learn a rule list for the data
  classifier = learner(training_data)

  print("Writing rules to file")
  # write rules to file
  rulesfile = "{}/rules.csv".format(output_dir)
  with open(rulesfile, 'w') as csvfile:
    rules = csv.writer(csvfile)
    # Create rules file from repaired data
    rules.writerow(["Label","Rules","Quality","Score"])
    for rule_num, rule in enumerate(classifier.rule_list):
      # calculate influence score
      domain = rule.domain.attributes
      selectors = rule.selectors
      score = sum([float(influence_scores[domain[s.column].name]) for s in selectors])
      # write rule details to file
      rules.writerow([rule_num, str(rule).strip(' '), rule.quality, score])

  print("Evaluating Model")
  test_data = Orange.data.Table.from_file(testfile)
  res = Orange.evaluation.TestOnTestData(training_data, test_data, [learner])
  accuracy = Orange.evaluation.scoring.CA(res)
  AUC = Orange.evaluation.scoring.AUC(res)
  return rulesfile, accuracy, AUC

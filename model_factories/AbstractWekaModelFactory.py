from abc import ABCMeta, abstractmethod
from AbstractModelFactory import AbstractModelFactory
from AbstractModelVisitor import AbstractModelVisitor

from collections import OrderedDict
import subprocess
import io
import csv
import os
import time

WEKA_PATH = "/usr/share/java/weka.jar"
TMP_DIR = "tmp/"

if not os.path.isfile(WEKA_PATH):
  raise Exception("WEKA_PATH is not properly set!")

# Create the TMP_DIR if it does not already exist.
if not os.path.exists(TMP_DIR):
  os.makedirs(TMP_DIR)

class AbstractWekaModelFactory(AbstractModelFactory):
  __metaclass__ = ABCMeta

  @abstractmethod
  def __init__(self, *args, **kwargs):
    super(AbstractWekaModelFactory, self).__init__(*args,**kwargs)
    self.train_command = ""
    self.model_visitor_type = None

  def build(self, train_set):

    # Prepare the ARFF file that will train the model.
    arff_types = get_arff_type_dict(self.headers, self.all_data,self.features_to_ignore)
    model_file = TMP_DIR + "{}_{}_{}.model".format(self.verbose_factory_name, self.factory_name, time.time())
    train_arff_file = model_file + ".train.arff"
    list_to_arff_file(self.headers,arff_types, train_set, train_arff_file)

    response_index = self.headers.index(self.response_header)

    # Call WEKA to generate the model file.
    command = "java {} -t {} -d {} -p 0 -c {}".format(self.train_command, train_arff_file, model_file, response_index + 1)
    run_weka_command(command)

    return self.model_visitor_type(model_file, arff_types, response_index, self.headers)


class AbstractWekaModelVisitor(AbstractModelVisitor):

  def __init__(self, model_name, arff_types, response_index, headers):
    self.model_name = model_name
    self.arff_types = arff_types
    self.response_index = response_index
    self.headers = headers
    self.test_command = ""

  def test(self, test_set, test_name=""):
    test_arff_file = "{}.{}.test.arff".format(self.model_name, test_name)
    list_to_arff_file(self.headers, self.arff_types, test_set, test_arff_file)
    results_path = "{}.out".format(test_arff_file)

    # Produce predictions for the test set.
    # Note: The "-c" option is 1-indexed by Weka
    command = "java {} -T {} -l {} -p 0 -c {} 1> {}".format(self.test_command, test_arff_file, self.model_name, self.response_index+1, results_path)
    run_weka_command(command)

    # Read the output file.
    prediction_index = 2
    with open(results_path, "r") as f:
      raw_lines = f.readlines()[5:-1] # Discard the headers and ending line.
      raw_predictions = [line.split()[prediction_index] for line in raw_lines]
      predictions = [prediction.split(":")[1] for prediction in raw_predictions]

    return zip([row[self.response_index] for row in test_set], predictions)


def run_weka_command(command):
  set_path = "export CLASSPATH=$CLASSPATH:{}; ".format(WEKA_PATH)
  subprocess.check_output(set_path + command, shell=True)


def get_arff_type_dict(headers, data, features_to_ignore=[]):
  values = {header:[row[i] for row in data] for i, header in enumerate(headers) if header not in features_to_ignore}
  arff_type = OrderedDict()
  for header in headers:
    if all( map(lambda x: isinstance(x, float), values[header]) ):
      arff_type[header] = "numeric"
    elif all( map(lambda x: isinstance(x, bool), values[header]) ):
      arff_type[header] = [True,False]
    elif all( map(lambda x: isinstance(x, int), values[header]) ):
      arff_type[header] = "numeric"
    else:
      arff_type[header] = sorted(set(values[header])) # Categorical
  return arff_type


def list_to_arff_file(headers, arff_type_dict, data, arff_file_output):
  def arff_format(string):
    # Remove empty strings and quote strings with spaces.
    if string == "":
      string = "N/A"
    return '"{}"'.format(string) if " " in str(string) else string

  # Produce the relevant file headers for the ARFF.
  arff_header = "@relation BlackBoxAuditing\n"
  for attribute, types in arff_type_dict.items():
    if type(types) == list:
      formatter = io.BytesIO()
      writer = csv.writer(formatter)
      unique_values = list(set(types))
      unique_values = [arff_format(val) for val in unique_values]
      writer.writerow(unique_values)
      formatted = formatter.getvalue().strip('\r\n')
      types = "{" + formatted + "}"
    attribute = attribute.replace(" ","_")
    types = types.replace('"""','"')
    arff_header += "@attribute {} {}\n".format(attribute, types)

  arff_header += "\n@data\n"

  # Write the data in a CSV-like format to avoid weird escaping issues.
  data_output = io.BytesIO()
  csv_writer = csv.writer(data_output)
  for row in data:
    row = [arff_format(val) for h, val in zip(headers,row) if h in arff_type_dict]
    csv_writer.writerow(row)

  # Dump everything into the intended ARFF file.
  with open(arff_file_output, "w") as f:
    output = data_output.getvalue().replace('"""','"')
    f.write(arff_header + output)

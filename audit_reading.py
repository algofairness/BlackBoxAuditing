import matplotlib.pyplot as plt
import json
import os
import random

def graph_audit(filename, measurement_calculators, output_image_file):
  with open(filename) as audit_file:
    header_line = audit_file.readline()[:-1] # Remove the trailing endline.

    # Extract the confusion matrices and repair levels from the audit file.
    confusion_matrices = []
    for line in audit_file:
      separator = ":"
      separator_index = line.index(separator)

      repair_level = float(line[:separator_index])
      raw_confusion_matrix = line[separator_index + len(separator):-1]
      confusion_matrix = json.loads( raw_confusion_matrix.replace("'","\"") )
      confusion_matrices.append( (repair_level, confusion_matrix) )

  # Sort the repair levels in case they are out of order for whatever reason.
  confusion_matrices.sort(key = lambda pair: pair[0])

  x_axis = [repair_level for repair_level, _ in confusion_matrices]

  # Graph the results for each requested measurement.
  for calculator in measurement_calculators:
    y_axis = [calculator(matrix) for _, matrix in confusion_matrices]
    plt.plot(x_axis, y_axis, label=calculator.__name__)

  plt.title(header_line)
  plt.axis([0,1,0,1.1]) # Make all the plots consistently sized.
  plt.xlabel("Repair Level")
  plt.legend()
  plt.savefig(output_image_file)


def test():
  TMP_DIR = "tmp"
  if not os.path.exists(TMP_DIR):
    os.makedirs(TMP_DIR)

  # Prepare the sample audit.
  audit_filename = TMP_DIR + "/test_audit.audit"
  with open(audit_filename, "w") as f:
    f.write("GFA Audit for: Test Feature\n0.0:{'A': {'B': 100}, 'B': {'B': 199}}\n0.1:{'A': {'B': 100}, 'B': {'B': 199}}\n0.2:{'A': {'B': 100}, 'B': {'B': 199}}\n0.3:{'A': {'B': 100}, 'B': {'B': 199}}\n0.4:{'A': {'B': 100}, 'B': {'B': 199}}\n0.5:{'A': {'B': 100}, 'B': {'B': 199}}\n0.6:{'A': {'B': 100}, 'B': {'B': 199}}\n0.7:{'A': {'B': 100}, 'B': {'B': 199}}\n0.8:{'A': {'B': 100}, 'B': {'B': 199}}\n0.9:{'A': {'B': 100}, 'B': {'B': 199}}\n1.0:{'A': {'B': 100}, 'B': {'B': 199}}\n")

  # A mock measurement calculator that returns a random number.
  def mock_measurement(conf_matrix):
    return random.random()

  # Perform the audit and save it an output image.
  calculators = [mock_measurement, mock_measurement]
  output_image = TMP_DIR + "/test_image.png"
  graph_audit(audit_filename, calculators, output_image)

  file_not_empty = os.path.getsize(output_image) > 0
  print "GradientFeatureAuditor -- image file generated? --", file_not_empty



if __name__=="__main__":
  test()

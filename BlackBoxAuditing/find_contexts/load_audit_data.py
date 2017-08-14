def convert_types(correct_types):
  converted_types = []
  for type in correct_types:
    if type == int or type == float:
      converted_types.append("c") # continuous if a number
    else:
      converted_types.append("d") # discrete if a string
  return converted_types

def generate_meta_data(headers, response_header, features_to_ignore):
  meta_data = []
  for feature in headers:
    if feature == response_header:
      meta_data.append("class")
    elif feature in features_to_ignore:
      meta_data.append("ignore")
    else:
      meta_data.append("")
  return meta_data

def generate_tab_data(headers, types, meta_data, data, output):
  tab_data = open(output, 'w')
  tab_data.write("\t".join(headers)+'\n')
  tab_data.write("\t".join(types)+'\n')
  tab_data.write("\t".join(meta_data)+'\n')

  for row in data:
    tab_data.write("\t".join(str(x) for x in row)+'\n')

def merge_data(orig_data, obscured_data, header, obscured_tag):
  merged_data = []

  obscured_header = [feature+obscured_tag for feature in header]
  merged_header = [None]*(len(header)+len(obscured_header))
  merged_header[::2] = header
  merged_header[1::2] = obscured_header
  merged_data.append(merged_header)
 
  for row_number, orig_row in enumerate(orig_data):
    obscured_row = obscured_data[row_number+1]
    merged_row = [None]*(len(orig_row)+len(obscured_row))
    merged_row[::2] = orig_row
    merged_row[1::2] = obscured_row
    merged_data.append(merged_row)

  return merged_data

def load(audit_params, OUTPUT_DIR):
  orig_train, orig_test, obscured_test, headers, response_header, features_to_ignore, correct_types, obscured_tag = audit_params

  # generate data needed for finding CN2 rules
  converted_types = convert_types(correct_types)
  meta_data = generate_meta_data(headers, response_header, features_to_ignore)
  
  orig_train_tab = OUTPUT_DIR+"/original_train.tab"
  generate_tab_data(headers, converted_types, meta_data, orig_train, orig_train_tab)

  orig_test_tab = OUTPUT_DIR+"/original_test.tab"
  generate_tab_data(headers, converted_types, meta_data, orig_test, orig_test_tab)
  
  # generate merged_data
  merged_data = merge_data(orig_test, obscured_test, headers, obscured_tag)

  return orig_train_tab, orig_test_tab, merged_data

from BlackBoxAuditing.model_factories.AbstractModelFactory import AbstractModelFactory
from BlackBoxAuditing.model_factories.AbstractModelVisitor import AbstractModelVisitor

from sklearn import neural_network
import numpy as np
import copy

class ModelFactory(AbstractModelFactory):
    def __init__(self, *args, **kwargs):
        # Default DecisionTreeClassifier params
        self.hidden_layer_sizes = (50,25,)
        self.activation = "relu"
        self.solver = "adam"
        self.alpha = 0.00001
        self.batch_size = "auto"
        self.learning_rate = "constant"
        self.learning_rate_init = 0.001
        self.max_iter = 1000
        self.random_state = 123
        self.shuffle = True
        self.feats_to_ignore = []

        if "options" in kwargs:
            options = kwargs["options"]
            if "hidden_layer_sizes" in options:
                self.hidden_layer_sizes = options.pop("hidden_layer_sizes")
            if "activation" in options:
                self.activation = options.pop("activation")
            if "solver" in options:
                self.solver = options.pop("solver")
            if "alpha" in options:
                self.alpha = options.pop("alpha")
            if "random_state" in options:
                self.random_state = options.pop("random_state")
            if "batch_size" in options:
                self.batch_size = options.pop("batch_size")
            if "learning_rate" in options:
                self.learning_rate = options.pop("learning_rate")
            if "learning_rate_init" in options:
                self.learning_rate_init = options.pop("learning_rate_init")
            if "max_iter" in options:
                self.max_iter = options.pop("max_iter")
            if "shuffle" in options:
                self.shuffle = options.pop("shuffle")
            if "feats_to_ignore" in options:
                self.feats_to_ignore = options.pop("feats_to_ignore")
 
        super(ModelFactory, self).__init__(*args, **kwargs)
        self.verbose_factory_name = "DecisionTree"


        # Maps each header to the values for it's column.
        self.col_vals = {header:{row[i] for row in self.all_data} for i, header in enumerate(self.headers)}
        self.response_index = self.headers.index(self.response_header)
        self.num_outcomes = len(self.col_vals[self.response_header])

        # Mark any categorical features for column expansion.
        # Categorical features are transfered into -1, 1 binary features for each value.
        self.columns_to_expand = []
        for i, header in enumerate(self.headers):
            categorical = any(type(val)==str for val in self.col_vals[header])
            if i == self.response_index or categorical:
                self.columns_to_expand.append(header)
    
        # All non-categorical features will be standardized (mean=0, variance=1).
        self.standardizers = {}
        for i, header in enumerate(self.headers):
            if any (type(row[i])==str for row in self.all_data):
                mean = None
                std_dev = None
            else:
                mean = sum(row[i] for row in self.all_data)/float(len(self.all_data))
                std_dev = np.sqrt(sum(((row[i] - mean) ** 2) for row in self.all_data)/float(len(self.all_data)))
            self.standardizers[header] = {'mean':mean, 'std_dev':std_dev}
        

        # If the response column is shifted by expanding categorical features, 
        # update the response index.
        response_col_shift = 0
        for header in self.headers[:self.response_index]:
            if header in self.columns_to_expand:
                response_col_shift += len(self.col_vals[header]) - 1
        self.adjusted_response_index = self.response_index + response_col_shift
    
        # Map each outcome to an index
        self.outcome_trans_dict = {val:i for i, val in enumerate(self.col_vals[self.response_header])}        
        



    def build(self, train_set):
        # prepare train data for learning
        if self.shuffle == True:
            np.random.seed(123)
            np.random.shuffle(train_set)
        expanded_and_stdized_train_set, self.expanded_headers = expand_and_standardize_dataset(self.response_index, self.response_header, train_set, self.col_vals, self.headers, self.standardizers, self.feats_to_ignore, self.columns_to_expand, self.outcome_trans_dict)
        train_matrix, train_outcomes = list_to_tf_input(expanded_and_stdized_train_set, self.adjusted_response_index, self.num_outcomes)
        train_size, num_features = train_matrix.shape
        
        clf = neural_network.MLPClassifier(
                hidden_layer_sizes=self.hidden_layer_sizes,\
                activation=self.activation,\
                solver=self.solver,\
                alpha=self.alpha,\
                batch_size=self.batch_size,\
                learning_rate=self.learning_rate,\
                learning_rate_init=self.learning_rate_init,\
                max_iter=self.max_iter,\
                random_state=self.random_state,\
                shuffle=self.shuffle
                ) 

        clf.fit(train_matrix, train_outcomes)
        model_name = "DecisionTreeModel"

        return(ModelVisitor(clf, model_name, self.response_header, self.response_index, self.adjusted_response_index, self.num_outcomes, self.outcome_trans_dict, self.headers, self.expanded_headers, self.standardizers, self.col_vals, self.feats_to_ignore, self.columns_to_expand))


class ModelVisitor(AbstractModelVisitor):

  def __init__(self, clf, model_name, response_header, response_index, adjusted_response_index, num_outcomes, outcome_trans_dict, headers, expanded_headers, standardizers, train_col_vals, feats_to_ignore, columns_to_expand):
    super(ModelVisitor,self).__init__(model_name)
    self.response_index = response_index
    self.response_header = response_header
    self.adjusted_response_index = adjusted_response_index
    self.num_outcomes = num_outcomes
    self.outcome_trans_dict = outcome_trans_dict
    self.headers = headers
    self.expanded_headers = expanded_headers
    self.train_expanded_headers = expanded_headers
    self.train_col_vals = train_col_vals
    self.standardizers = standardizers
    self.feats_to_ignore = feats_to_ignore
    self.columns_to_expand = columns_to_expand
    self.clf = clf

  def test(self, test_set, test_name=""):
    expanded_and_stdized_test_set, self.test_set_expanded_headers = expand_and_standardize_dataset(self.response_index, self.response_header, test_set, self.train_col_vals, self.headers, self.standardizers, self.feats_to_ignore, self.columns_to_expand, self.outcome_trans_dict)
    if self.test_set_expanded_headers != self.train_expanded_headers:
      raise ValueError('Feature dimensions do not align!')
    else:
      test_matrix, test_labels = list_to_tf_input(expanded_and_stdized_test_set, self.adjusted_response_index, self.num_outcomes)

   
    predictions = self.clf.predict(test_matrix)
    predictions, test_labels = predictions.tolist(), test_labels.tolist() # cast from numpy array to python list
    test_labels = [(corr[0], corr[1]) for corr in test_labels]
    predictions = [row.index(1) for row in predictions]
    predictions_dict = {i:key for key,i in list(self.outcome_trans_dict.items())}
    predictions = [predictions_dict[pred] for pred in predictions]
    return list(zip([row[self.response_index] for row in test_set], predictions))


def list_to_tf_input(data, response_index, num_outcomes):
  """
  Separates the outcome feature from the data and creates the onehot vector for each row.
  """
  matrix = np.matrix([row[:response_index] + row[response_index+1:] for row in data])
  outcomes = np.asarray([row[response_index] for row in data], dtype=np.uint8)
  outcomes_onehot = (np.arange(num_outcomes) == outcomes[:, None]).astype(np.float32)

  return matrix, outcomes_onehot

def expand_and_standardize_dataset(response_index, response_header, data_set, col_vals, headers, standardizers, feats_to_ignore, columns_to_expand, outcome_trans_dict):
  """
  Standardizes continuous features and expands categorical features.
  """
  # expand and standardize
  modified_set = []
  for row_index, row in enumerate(data_set):
    new_row = []
    for col_index, val in enumerate(row):
      header = headers[col_index]

      # Outcome feature -> index outcome
      if col_index == response_index:
        new_outcome = outcome_trans_dict[val]
        new_row.append(new_outcome)

      # Ignored feature -> pass
      elif header in feats_to_ignore:
        pass
      
      # Categorical feature -> create new binary column for each possible value of the column
      elif header in columns_to_expand:
        for poss_val in col_vals[header]:
          if val == poss_val:
            new_cat_val = 1.0
          else:
            new_cat_val = -1.0
          new_row.append(new_cat_val)

      # Continuous feature -> standardize value with respect to its column
      else:
        new_cont_val = float((val - standardizers[header]['mean']) / standardizers[header]['std_dev'])
        new_row.append(new_cont_val)

    modified_set.append(new_row)

  # update headers to reflect column expansion
  expanded_headers = []
  for header in headers:
    if header in feats_to_ignore:
      pass
    elif (header in columns_to_expand) and (header is not response_header):
      for poss_val in col_vals[header]:
        new_header = '{}_{}'.format(header,poss_val)
        expanded_headers.append(new_header)
    else:
      expanded_headers.append(header)

  return modified_set, expanded_headers

def test():
  test_expand_and_standardize_dataset()
  test_unseen_categorical_feature()
  test_categorical_model()
  test_categorical_response()
  test_list_to_tf_input()
  test_basic_model()
  test_simple_data()

def test_expand_and_standardize_dataset():
  """
  Tests if the function correctly converts categorical
  features into onehot features, correctly standardizes 
  continuous features, and correctly converts the response
  feature to indexes.
  """
  headers = ['cont_feature', 'cat_feature', 'ignored', 'response']
  data = [[75., 'A', 'ingore1', 'X'], [25, 'B', 'ignore2', 'Y'], [75, 'C', 'ignore3', 'Z'], [25., 'A', 'ignore1', 'Y']]
  resp_index = 3
  resp_header = 'response'
  feats_to_ignore = 'ignored'
  col_vals = {'cont_feature':[75., 25.], 'cat_feature':['A','B','C'], 'ignored':['ignore1', 'ignore2', 'ignore3'], 'response':['X', 'Y', 'Z']}
  columns_to_expand = ['cat_feature', 'ignored', 'response']
  outcome_trans_dict = {'X':0, 'Y':1, 'Z':2}
  standardizers = {'cont_feature':{'mean':50, 'std_dev':25}}
  new_data, new_headers = expand_and_standardize_dataset(resp_index, resp_header, data, col_vals, headers, standardizers, feats_to_ignore, columns_to_expand, outcome_trans_dict)
  correct_data = [[1.0, 1.0, -1.0, -1.0, 0], [-1.0, -1.0, 1.0, -1.0, 1], [1.0, -1.0, -1.0, 1.0, 2], [-1.0, 1.0, -1.0, -1.0, 1]]
  correct_headers = ['cont_feature', 'cat_feature_A', 'cat_feature_B', 'cat_feature_C', 'response']
  print('expanding and standardizing data correctly? --', new_data==correct_data)
  print('expanding headers correctly? --', new_headers==correct_headers)

def test_unseen_categorical_feature():
  """
  Tests if the model can correctly handle unfamiliar values
  for categorical features. The model should not create new onehot 
  features for values in the test set and should instead treat
  these values as 'not any known value for that column'. 
  """
  headers = ["predictor 1", "predictor 2", "predictor3", "response"]
  response = "response"
  random_features = ['H', 5.5, 'I']
  train_set = [[random_features[i%3],'B',1,'C'] for i in range(1,50)] + [['A','A',-1,'D'] for i in range(1,50)]
  train_set_copy = copy.copy(train_set)
  new_features = ['J',9]
  test_set = [[new_features[i%2],'B',1,'C'] for i in range(1,49)] + [['A','A',-1,'D'] for i in range(1,50)]
  all_data = train_set + test_set

  factory = ModelFactory(all_data, headers, response, name_prefix="test")
  model = factory.build(train_set)
  print("factory builds ModelVisitor? -- ", isinstance(model, ModelVisitor))

  predictions = model.test(test_set)
  print("handling unseen categorical values correctly? -- ", all([pred[0] == pred[1] for pred in predictions]))


def test_list_to_tf_input():
  data = [[0,0],[0,1],[0,2]]
  tf_matrix, tf_onehot = list_to_tf_input(data, 1, 3)
  correct_matrix = [[0],[0],[0]]
  correct_onehot = [[1,0,0], [0,1,0], [0,0,1]]
  print("list_to_tf_input matrix correct? --",np.array_equal(tf_matrix, correct_matrix))
  print("list_to_tf_input onehot correct? --",np.array_equal(tf_onehot, correct_onehot))

def test_basic_model():
  headers = ["predictor 1", "predictor 2", "response"]
  response = "response"
  train_set = [[i,0,0] for i in range(1,50)] + [[0,i,1] for i in range(1,50)]
  test_set = [[i,0,0] for i in range(1,50)] + [[0,i,1] for i in range(1,50)]
  all_data = train_set + test_set

  factory = ModelFactory(all_data, headers, response, name_prefix="test")

  model = factory.build(train_set)

  predictions = model.test(test_set)
  intended_predictions = [pred[0] for pred in predictions]
  actual_predictions = [pred[1] for pred in predictions]
  print("predicting numeric categories correctly? -- ", actual_predictions == intended_predictions)

def test_categorical_response():
  headers = ["predictor 1", "predictor 2", "response"]
  response = "response"
  train_set = [[i,0,"A"] for i in range(1,50)] + [[0,i,"B"] for i in range(1,50)]
  test_set = [[i,0,"A"] for i in range(1,50)] + [[0,i,"C"] for i in range(1,50)]
  train_set_copy = copy.copy(train_set)
  test_set_copy = copy.copy(test_set)
  all_data = train_set + test_set

  factory = ModelFactory(all_data, headers, response, name_prefix="test")
  model = factory.build(train_set)

  predictions = model.test(test_set)
  resp_index = headers.index(response)
  intended_predictions = [(test_row[resp_index], train_row[resp_index]) for train_row, test_row in zip(train_set_copy,test_set_copy)]
  print("predicting string-categories correctly? -- ", predictions == intended_predictions)

def test_categorical_model():
  """
  Tests whether the model can correctly learn on the train set. 
  The model should have poor accuracy on the test set
  because the outcomes do not match those of the train set.
  The model should incorrectly predict response 'B' for predictor 'B'
  when response 'C' is the correct response.
  """
  headers = ["predictor", "response"]
  response = "response"
  train_set = [["A","A"] for i in range(1,50)] + [["B","B"] for i in range(1,50)]
  train_set_copy = copy.copy(train_set)
  test_set = [["A","A"] for i in range(1,50)] + [["B","C"] for i in range(1,50)]
  all_data = train_set + test_set
  factory = ModelFactory(all_data, headers, response, name_prefix="test", options={})

  model = factory.build(train_set)

  predictions = model.test(test_set)
  resp_index = headers.index(response)
  intended_predictions = [(test_row[resp_index], train_row[resp_index]) for train_row, test_row in zip(train_set_copy,test_set)]
  print("predicting string-categories correctly? -- ", predictions == intended_predictions)

def test_simple_data():
    headers = ["predictor_1", "predictor_2", "response"]
    response = "response"
    
    train_set = [["A","B","C"] for i in range(1,50)] + [["B","A","D"] for i in range(1,50)] + [["B","B","E"] for i in range(1,50)] + [["A", "A", "E"] for i in range(1,50)] + [["C", "D", "F"] for i in range(1,10)]
    train_set_copy = copy.copy(train_set) 
    test_set = [["A","B","C"] for i in range(1,50)] + [["B","A","D"] for i in range(1,50)] + [["B","B","E"] for i in range(1,50)] + [["A", "A", "E"] for i in range(1,50)] + [["A","X","Y"] for i in range(1,10)]
    all_data = train_set + test_set
    factory = ModelFactory(all_data, headers, response, name_prefix="test", options={})

    model = factory.build(train_set)
    predictions = model.test(test_set)
    resp_index = headers.index(response)
    
    intended_predictions = [(test_row[resp_index], train_row[resp_index]) for train_row, test_row in zip(train_set_copy,test_set)]
    last_few_preds = all(pred[0] == pred[1] for pred in predictions[-9:]) 
    all_but_last_few = all(pred[0] == pred[1] for pred in predictions[:-9])
    print("handling simple data correctly? -- ", (all_but_last_few and not last_few_preds) == True)

if __name__=='__main__':
  test()



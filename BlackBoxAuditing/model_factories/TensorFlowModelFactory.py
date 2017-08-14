"""
To reproduce results from the "Auditing Black-box Models for Indirect Influence" 
paper (11/30/2016), set model_options in main.py to {'reproduce':True} 
"""

from BlackBoxAuditing.model_factories.AbstractModelFactory import AbstractModelFactory
from BlackBoxAuditing.model_factories.AbstractModelVisitor import AbstractModelVisitor

import os
import numpy as np
import random as rand
import tensorflow as tf
import copy
import time

TMP_DIR_HOST = 'tmp'

date_stamp = time.strftime('%a.%d.%b_%S.%M.%H', time.localtime())
log_dir = '{}/{}__{}'.format(TMP_DIR_HOST, date_stamp, rand.randint(1,1000000))
os.makedirs(log_dir)  


class ModelFactory(AbstractModelFactory):
  def __init__(self, *args, **kwargs):
    self.num_epochs = 500          # number of passes through training data
    self.batch_size = 20            # number of points trained on per step
    self.learning_rate = .01            # learning rate for optimizer
    self.beta1_decay = 0.95              # see Tensorflow's documentation for tf.train.AdamOptimizer
    self.beta2_decay = 0.99                # for information on beta decay
    self.epsilon = 1e-8                 # small number for stability of optimizer
    self.init_shuffle = True           # shuffle data before training starts
    self.iter_shuffle = True           # shuffle batch for each step
    self.feats_to_ignore = []           # features to ignore during training
    self.hidden_layer_sizes = []        # if empty, no hidden layers are used
    self.constant_descent = False       # flag to implement tf.GradientDescentOptimizer

    # Set manual settings.
    if 'options' in kwargs:
      options = kwargs['options']
      if 'num_epochs' in options:
        self.num_epochs = options.pop('num_epochs')
      if 'batch_size' in options:
        self.batch_size = options.pop('batch_size')
      if 'learning_rate' in options:
        self.learning_rate = options.pop('learning_rate')
      if 'beta1_decay' in options:
        self.beta1_decay = options.pop('beta1_decay')
      if 'beta2_decay' in options:
        self.beta2_decay = options.pop('beta2_decay')
      if 'epsilon' in options:
        self.epsilon = options.pop('epsilon')
      if 'init_shuffle' in options:
        self.init_shuffle = options.pop('init_shuffle')
      if 'iter_shuffle' in options:
        self.iter_shuffle = options.pop('iter_shuffle')
      if 'feats_to_ignore' in options:
        self.feats_to_ignore = options.pop('feats_to_ignore')
      if 'hidden_layer_sizes' in options:
        self.hidden_layer_sizes = options.pop('hidden_layer_sizes')
      if 'reproduce' in options:
        reproduce = options.pop('reproduce')
        if reproduce:
          self.num_epochs = 100
          self.batch_size = 100
          self.learning_rate = 0.01
          self.hidden_layer_sizes = []
          self.init_shuffle = False
          self.iter_shuffle = False
          self.constant_descent = True

    # Initiate inheritance
    super(ModelFactory, self).__init__(*args, **kwargs)
    self.verbose_factory_name = 'TensorFlow_Network'


    # Maps each header to all possible values for it's column.
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
    model_name="{}/{}_{}_{}.model".format(log_dir, self.verbose_factory_name, self.factory_name, time.time())
    # prepare train data for learning
    if self.init_shuffle == True:
      np.random.seed(123)
      np.random.shuffle(train_set)
    expanded_and_stdized_train_set, self.expanded_headers = expand_and_standardize_dataset(self.response_index, self.response_header, train_set, self.col_vals, self.headers, self.standardizers, self.feats_to_ignore, self.columns_to_expand, self.outcome_trans_dict)
    train_matrix, train_outcomes = list_to_tf_input(expanded_and_stdized_train_set, self.adjusted_response_index, self.num_outcomes)
    train_size, num_features = train_matrix.shape
    
    # Ensure there are no pre-existing nodes in the tensorflow graph.
    tf.reset_default_graph()
    
    # input and output nodes
    with tf.name_scope('input'):
      x = tf.placeholder(tf.float32, shape=[None, num_features], name='x_input') # Input
      y_ = tf.placeholder(tf.float32, shape=[None, self.num_outcomes], name='y_input') # Correct Output
    
    # Construct the layer architecture.
    # Generate a layer for the input and for each additional hidden layer.
    layer_sizes = [num_features] + self.hidden_layer_sizes + [self.num_outcomes]
    layers = [x] # Count the input as the first layer
    for i in range(len(layer_sizes) - 1):
      layer_size = layer_sizes[i]
      prev_layer = layers[-1]
      next_layer_size = layer_sizes[i+1]
      
      # Create a new layer with initially random weights and biases.  
      if i == len(layer_sizes) - 1:   # Final layer is output.
        layer_name = 'output'
      else:
        layer_name = 'hidden_layer_{}'.format(i)
      with tf.name_scope(layer_name):
        tf.set_random_seed(123)
        W = tf.Variable(tf.random_normal([layer_size, next_layer_size]), name='weights')
        b = tf.Variable(tf.random_normal([next_layer_size]), name='biases')
        new_layer = (tf.add(tf.matmul(prev_layer, W),b))  # Wx + b
        layers.append(new_layer)

    y = layers[-1]

    # Optimization.
    with tf.name_scope('accuracy'):
      correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
      accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))  
    with tf.name_scope('cross_entropy'):
      cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y, labels=y_))
    with tf.name_scope('train_step'):
      if self.constant_descent:
        train_step = tf.train.GradientDescentOptimizer(learning_rate = self.learning_rate, name='Gradient_Descent').minimize(cross_entropy)
      else:
        train_step = tf.train.AdamOptimizer(learning_rate=self.learning_rate, beta1=self.beta1_decay, beta2=self.beta2_decay, epsilon=self.epsilon, name='Adam_Optimizer').minimize(cross_entropy)
      

    # Summaries for TensorBoard
    tf.summary.scalar('accuracy', accuracy)
    tf.summary.scalar('entropy', cross_entropy)

    saver = tf.train.Saver()
    merge = tf.summary.merge_all()
    
    with tf.Session() as sess:

      writer = tf.summary.FileWriter(log_dir, graph=sess.graph)
      tf.global_variables_initializer().run()
      num_steps = self.num_epochs * train_size // self.batch_size
      for step in range(num_steps):
        # get batch
        offset = (step * self.batch_size) % train_size
        batch_data = train_matrix[offset:(offset + self.batch_size), :]
        batch_labels = train_outcomes[offset:(offset + self.batch_size)]

        # shuffle
        if self.iter_shuffle == True:
          np.random.seed(step)
          rng_state = np.random.get_state()
          np.random.shuffle(batch_data)
          np.random.set_state(rng_state)
          np.random.shuffle(batch_labels)
        # train and write summary
        _, summary = sess.run([train_step, merge], feed_dict={x:batch_data, y_:batch_labels})
        writer.add_summary(summary, global_step=step+1)
        # Save checkpoints every 1000 steps
        if step % 50 == 0:
          model_name="{}/{}_{}_{}.model".format(log_dir, self.verbose_factory_name, self.factory_name, time.time())
          checkpoint = saver.save(sess, model_name, global_step=step+1)

      # Save checkpoint upon completion of training
      model_name="{}/{}_{}_{}.model".format(log_dir, self.verbose_factory_name, self.factory_name, time.time())
      checkpoint = saver.save(sess, model_name, global_step=num_steps)

      # print 'Train Accuracy:', accuracy.eval(feed_dict={x:train_matrix, y_:train_outcomes})

    return ModelVisitor(model_name, checkpoint, saver, self.response_header, self.response_index, self.adjusted_response_index, self.num_outcomes, x, y_, y, self.outcome_trans_dict, self.headers, self.expanded_headers, self.standardizers, self.col_vals, self.feats_to_ignore, self.columns_to_expand)


class ModelVisitor(AbstractModelVisitor):

  def __init__(self, model_name, checkpoint, model_saver, response_header, response_index, adjusted_response_index, num_outcomes, x, y_, y, outcome_trans_dict, headers, expanded_headers, standardizers, train_col_vals, feats_to_ignore, columns_to_expand):
    super(ModelVisitor,self).__init__(model_name)
    self.model_saver = model_saver
    self.checkpoint = checkpoint
    self.response_index = response_index
    self.response_header = response_header
    self.adjusted_response_index = adjusted_response_index
    self.num_outcomes = num_outcomes
    self.x = x
    self.y_ = y_
    self.y = y
    self.outcome_trans_dict = outcome_trans_dict
    self.headers = headers
    self.expanded_headers = expanded_headers
    self.train_expanded_headers = expanded_headers
    self.train_col_vals = train_col_vals
    self.standardizers = standardizers
    self.feats_to_ignore = feats_to_ignore
    self.columns_to_expand = columns_to_expand

  def test(self, test_set, test_name=""):
    expanded_and_stdized_test_set, self.test_set_expanded_headers = expand_and_standardize_dataset(self.response_index, self.response_header, test_set, self.train_col_vals, self.headers, self.standardizers, self.feats_to_ignore, self.columns_to_expand, self.outcome_trans_dict)
    if self.test_set_expanded_headers != self.train_expanded_headers:
      raise ValueError('Feature dimensions do not align!')
    else:
      test_matrix, test_labels = list_to_tf_input(expanded_and_stdized_test_set, self.adjusted_response_index, self.num_outcomes)

    with tf.Session() as sess:
   
      self.model_saver.restore(sess, self.checkpoint)
      predictions = tf.argmax(self.y, 1).eval(feed_dict={self.x: test_matrix, self.y_:test_labels}, session=sess)

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

if __name__=='__main__':
  test()

# Black Box Auditing and Certifying and Removing Disparate Impact

This repository contains a sample implementation of Gradient Feature Auditing (GFA) meant to be generalizable to most datasets.  For more information on the repair process, see our paper on [Certifying and Removing Disparate Impact](http://arxiv.org/abs/1412.3756).  For information on the full auditing process, see our paper on [Auditing Black-box Models for Indirect Influence](http://arxiv.org/abs/1602.07043).

# License

This code is licensed under an [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0.html) license.

# Setup and Installation

1. Install pip3 if you do not already have it installed
2. Install BlackBoxAuditing (`pip3 install BlackBoxAuditing`)

# Certifying and Removing Disparate Impact

After installing BlackBoxAuditing, you can run the data repair described in [Certifying and Removing Disparate Impact](http://arxiv.org/abs/1412.3756) using the command `BlackBoxAuditing-repair` on a terminal which will tell you the arguments the script takes. The required arguments are input_csv, output_csv, repair_level, and kdd. There is a required flag -p (--protected) which designates the protected feature(s). An optional flag -i (--ignored) designates features to ignore during the repair process. 

```
# repair german.csv with respect to "age" at repair level 0.5, ignoring "occupation".
BlackBoxAuditing-repair german_categorical.csv repaired_german.csv 0.5 True -p "age" -i "occupation"

# repair your_data.csv with respect to "feat1" and "feat2" at repair level 0.8.
BlackBoxAuditing-repair your_data.csv repaired_data.csv 0.8 False -p "feat1" "feat2"
```

# Black Box Auditing

The below instructions focus on running GFA on a dataset (as in [Auditing Black-box Models for Indirect Influence](http://arxiv.org/abs/1602.07043)).  There is also a [tutorial](https://algofairness.github.io/fatconference-2018-auditing-tutorial/) (with a jupyter notebook) from FAT* 2018 and a [video](https://www.youtube.com/watch?v=rtDkl_0vLks) of the tutorial.


## Running as a Python Script

After installing BlackBoxAuditing, GFA can be run on a dataset (as in [Auditing Black-box Models for Indirect Influence](http://arxiv.org/abs/1602.07043)) using a simple python script. For reference, the following includes sample code:

```python3
%python
# import BlackBoxAuditing
import BlackBoxAuditing as BBA
# import machine learning technique
from BlackBoxAuditing.model_factories import SVM, DecisionTree, NeuralNetwork

"""
Using a preloaded dataset
"""
# load in preloaded dataset
data = BBA.load_data("german")

# initialize the auditor and set parameters
auditor = BBA.Auditor()
auditor.ModelFactory= SVM

# call the auditor with the data
auditor(data, output_dir="german_audit_output")

# find contexts of discrimination in dataset
auditor.find_contexts("age_cat", output_dir="german_context_output")

"""
Using your own dataset
"""
# load your own data
datafile = 'path/to/datafile'
data = BBA.load_from_file(datafile)

# initialize the auditor and set parameters
auditor = BBA.Auditor()
auditor.ModelFactory= DecisionTree

# call the auditor with the data
auditor(data, output_dir="german_audit_output")

# find contexts of discrimination in dataset
auditor.find_contexts("age_cat", output_dir="german_context_output")

```

## Outputs of the Auditor
### Auditing with Repair Steps

Calling the auditor on a dataset will evaluate the predictive ability of a model at different repair steps for each feature. The auditor will create a subdirectory "<your data>_audit_output" in the directory from which you run the auditor. This directory will contain three summary files: accuracy.png, BCR.png, and summary.txt. The two graphical summaries, accuracy.png and BCR.png, show the predictive ability of the model at different repair levels for each repaired feature, using accuracy and BCR respectively as metrics. Non-graphical summaries of the audit are included in the summary.txt file. This file includes the model options used, which features were repaired, and ranks the features by the amount repair with respect to each feature affects the accuracy of the model. Approximate trend groups are also included in the summary.txt file, indicating the groups of features with similar trends in the repair steps. More detailed reports of the repair with respect to each of the features are included in the remaining files of the output.

### Finding Contexts

Calling the find_contexts() method of the auditor will train a model to determine rule-based contexts for classification in the dataset. The method create a subdirectory "<your data>_context_output" in the directory from which you run the auditor. This directory contains a file named contexts.summary. This file includes the model options used, and the contexts of influence found in the data. The directory also contains expanded rules


## More Advanced Script Options

#### Using a preloaded dataset

The BlackBoxAuditing package has a few datasets preloaded and ready to use for auditing. In a script, they are available via the function `load_data` which takes as input the name of the dataset and returns formatted data ready for auditing. The following is the list of preloaded datasets available for auditing:

* adult
* diabetes
* ricci
* german
* glass
* sample
* DRP
* SAT

Refer to the Sources section down below for more information about the datasets

#### Using you own dataset

To use your own data for auditing, the function `load_from_file`, most simply, takes as input the path to your dataset and returns formatted data ready for auditing. `load_from_file` also includes other paramters which should be set to ensure that your data is processed correctly. Refer to the full function and its defaults:

```
load_from_file(datafile, testdata=None, correct_types=None, train_percentage=2.0/3.0,
                   response_header=None, features_to_ignore=None, missing_data_symbol=""
```

* *datafile*: path to your dataset
* *testdata*: path to the dataset used for testing a model. Assumes that *datafile* is the training dtata
* *correct_types*: list of the types (str, int, or float) of the features in the data. If not given, the types will be automatically generated by inspecting the values of each feature
* *train_percentage*: train/test split of the data given as floats
* *response_header*: name of the response column in the data. if not given, assumes that the last column in the data is the response
* *features_to_ignore*: list of the names of any feature than you wish to be ignored by the model
* *missing_data_symbol*: symbol that marks missing or unknown value in the data

#### Auditor setup options

After initializing the auditor `auditor = BlackBoxAuditor.Auditor()`, there are a few options that can be set to tune the auditor listed as follows:

`auditor.measurers`: (*default = [accuracy, BCR]*) list of measurers to use for GFA

`auditor.model_options`: (*default = {}*) options for machine learning model

`auditor.verbose`: (*default = True*) Set to "True" to allow for more detailed status updates

`auditor.REPAIR_STEPS`: (*default = 10*) Number of repair steps take 

`auditor.RETRAIN_MODEL_PER_REPAIR`: (*default = False*) 

`auditor.WRITE_ORIGINAL_PREDICTIONS`: (*default = True*)

`auditor.ModelFactory`: (*default = SVM*) Available machine learning options: SVM, DecisionTree, NeuralNetwork

`auditor.kdd`: (*default = False*) 

`auditor.reapir_mode`: (*default = "Orig"*) Available repair methods: "Orig": when getting the median within buckets, only considers the values within the bucket, only considers said medians when getting the medians between buckets. "AllMed": when getting the median within buckets, considers all values of that feature between the minimum and maximum in the bucket, and does the same when getting the medians between buckets. "UMed": same as AllMed except it only considers unique values. "Mode": within buckets, is identical to "Orig", but between buckets, gets the mode of the medians. "Spec": spec allows you to choose whether to repair the data to the group with the highest median or the one with the loweat median by changing self.spec_group to "high" or "low"

`auditor.spec_group`: (*default = None) If repair_mode is "Spec", must be set to "high" or "low". If not set, will default to "high".

#### Auditor call options

Once the auditor is initialized and tuned `auditor = BlackBoxAuditor.Auditor()`, there are a few options that can be set to configure how the audit is run. Refer to the full audit call and its defaults:

```
auditor(data, output_dir=None, dump_all=False, features_to_audit=None, print_all_data=False, make_all_graphs=False)
```

* *data*: data object returned from calling either `load_data' or `load_from_file`
* *output_dir*: name of the directory that audit files will be dumped to. If no output directory is specified, the program will not save anything to file
* *dump_all*: boolean value. If True, all files generated by the audit will be dumped including all original and repaired files, predictions files, audit files, and graphs. If False, only audit files and full repaired files will be dumped.
* *features_to_audit*: list of specific features that should be audited. If none specified, all features will be audited
* *print_all_data*: boolean value. If True and there is not output_dir, all data that would be saved is printed. If False, only summary data is printed.
* *make_all_graphs*: boolean value. If True, audit_directory is run and graphs are made.

#### Finding Contexts of Influence

`find_contexts` uses a CN2 rule learner to learn a rule list for the data and then uses both the rule list and information from a full audit to extract groups of features that have significant influence on the response label in the context of a given feature of interest. 
 
Completing a full audit is required before calling find_contexts. Calling find_contexts on a partial audit will raise a `RuntimeError`. Refer to the following function call and its defaults:

```
find_contexts(removed_attr, output_dir, beam_width=10, min_covered_examples=1, max_rule_length=5, by_original=True, epsilon=0.05)
```

* *removed_attr*: name of the feature which the contexts of influence will be found with respect to. Audited data obscured with respect to this feature will be used. 
* *output_dir*: name of the directory that the context results will be dumped to.
* *beam_width*: the number of solution streams considered at one time when searching for rules in the CN2 algorithm.
* *min_covered_examples*: the minimum number of examples a found rule must cover to be considered as an addition to the rule list.
* *max_rule_length*: the maximum number of conditions that found rules may combine.
* *by_original*: consider the best expanded rule within epsilon of original quality (True) or best quality of expanded rules (False).
* *epsilon*: Number within which we consider best expanded rule of the original quality.

#### Making Distributions

Setting make_all_graphs to True or running audit_directory on an output directory will create graphs comparing the accuracy and BCR or different features as well as the distributions for all possible combinations of features with the given data. In order to graph a specific distribution, one can call `graph_particular_distribution`:

```
graph_particular_distribution(directory, file, response_header, num_feat_index, only_groups=None)
```

* *directory*: name of the output directory that contains the files to be graphed.
* *file*: name of the file for the repaired data.
* *response_header*: the header for the response feature.
* *num_feat_index*: the index of the numerical feature to be graphed.
* *only_groups*: a list of the names of the groups to be graphed. If left blank, all groups will be graphed.

## Testing Code Changes

After BlackBoxAuditing has been installed, you can run the test suite using the command on a terminal `BlackBoxAuditing-test`.

Every python file should include test functions at the bottom that will be run when the file is run. This can be done by including the line `if __name__=="__main__": test()` as long as there is a function defined as `test`.

These tests should use print statements with `True` or `False` readouts indicating success or failure (where `True` should always be success). It is fine/good to have multiple of these per file.

Note: if a test requires reading data from the `test_data` directory, it should import the appropriate `load_data` file from the `experiments` directory.

## Implementing a New Machine-Learning Method

The best way to create a model would be to use a ModelFactory and ModelVisitors. A ModelVisitor should be thought of as a wrapper that knows how to load a machine-learning model of a given type and communicate with that model file in order to output predicted values of some test dataset. A ModelFactory simply knows how to "build" a ModelVisitor based on some provided training data. Check out the "Abstract" files in the `sample_experiment` directory for outlines of what these two classes should do.

# For local developers

## Upload a new version of BBA

The following details instructions for uploading an updated version of BBA to PyPi. If you do not have twine and setuptools installs, install them with the following commands:

```
pip install twine
pip install -U pip setuptools
```
Once all changes to the code have been tested, update the version number of BBA in `BlackBoxAuditing/setup.py` by modifying the variable `VERSION`.

If any non-python files were added to BBA that need to be included in the updated distribution, be sure to include them in the file `BlackBoxAuditing/MANIFEST.in`. Also update the `BlackBoxAuditing/requirements.txt` if necessary.

To create the source distribution of the project, run the following command:

```
python3 setup.py sdist
```

This will add the distribution to a directory `dist/`. Once the source distribution has been created, upload it PyPi using twine:

```
twine upload dist/BlackBoxAuditing-0.x.y.tar.gz
```

where 0.x.y is the version number of the updated project. This will prompt the user to input the username and password of the pypi account under which BBA is registered.

For more information and details for distributing a python project with twine, visit https://packaging.python.org/tutorials/distributing-packages/.

# Sources

Dataset Sources:
 - adult.csv [link](https://archive.ics.uci.edu/ml/datasets/Adult)
 - german_categorical.csv (Modified from [link](https://archive.ics.uci.edu/ml/datasets/Statlog+(German+Credit+Data))
 - RicciDataMod.csv (Modified from [link](http://www.amstat.org/publications/jse/v18n3/RicciData.csv))
 - DRP Datasets (Source and data-files coming soon.)
 - Arrests/Recidivism Datasets [link](http://www.icpsr.umich.edu/icpsrweb/RCMD/studies/3355)
 - Linear Datasets ("sample_2" Experiment) [link](https://github.com/jasonbaldridge/try-tf)

More information on DRP can be found at the [Dark Reactions Project](http://darkreactions.haverford.edu/) official site.

# Bug Reports and Feature-Requests

All bug reports and feature-requests should be submitted through the [Issue Tracker](https://github.com/cfalk/BlackBoxAuditing/issues).

# Black Box Auditing

This repository contains a sample implementation of Gradient Feature Auditing meant to be generalizable to most datasets.

For an example implementation, see (or run) the main.py file.

# Testing

All tests should be run from the main project directory. To make this process easier, a `run_test_suite.sh` file has been included (which can be run with bash via: `bash ./run_test_suite.sh`) in order to run all available tests at once.

Every python file should include test functions at the bottom that will be run when the file is run. This can be done by including the line `if __name__=="__main__": test()` as long as there is a function defined as `test`.

These tests should use print statements with `True` or `False` readouts indicating success or failure (where `True` should always be success). It is fine/good to have multiple of these per file.

Note: if a test requires reading data from the `test_data` file, it should import the necessary `load_data` file from the `experiments` directory.

# Creating New Types of ML-Models

The best way to create a model would be to use a ModelFactory and ModelVisitors. A ModelVisitor should be thought of as a wrapper that knows how to load a model of a given type and communicate with that model file in order to output predicted values of some test dataset. A ModelFactory simply knows how to "build" a ModelVisitor based on some provided training data. Check out the "Abstract" files in the `sample_experiment` directory for outlines of what these two classes should do; similarly, check out the "SVMModelFactory" files in the `sample_experiment` subdirectory for examples that use WEKA to create model files and produce predictions.

# Sources

DRP information (and the dataset) can be found at [Dark Reactions Project Moodle Group](https://moodlegroups.haverford.edu/course/view.php?id=65).

Dataset Sources:
 - adult.csv [link](https://archive.ics.uci.edu/ml/datasets/Adult)
 - german_categorical.csv & german.csv [link](https://archive.ics.uci.edu/ml/datasets/Statlog+(German+Credit+Data))
 - RicciDataMod.csv (Modified from [link](http://www.amstat.org/publications/jse/v18n3/RicciData.csv))

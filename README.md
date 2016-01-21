# Black Box Auditing

This repository contains a sample implementation of Gradient Feature Auditing meant to be generalizable to most datasets.

For an example implementation, see (or run) the main.py file.

# Creating New Types of ML-Models

The best way to create a model would be to use a ModelFactory and ModelVisitors. A ModelVisitor should be thought of as a wrapper that knows how to load a model of a given type and communicate with that model file in order to output predicted values of some test dataset. A ModelFactory simply knows how to "build" a ModelVisitor based on some provided training data. Check out the "Abstract" files in the DRP directory for outlines of what these two classes should do; similarly, check out the "SVMModel" files in the DRP subdirectory for examples that use WEKA to create model files and produce predictions.

# Sources

DRP information (and the dataset) can be found at [Dark Reactions Project Moodle Group](https://moodlegroups.haverford.edu/course/view.php?id=65).

Dataset Sources:
 - adult.csv [link](https://archive.ics.uci.edu/ml/datasets/Adult)
 - german_categorical.csv & german.csv [link](https://archive.ics.uci.edu/ml/datasets/Statlog+(German+Credit+Data))
 - RicciDataMod.csv (Modified from [link](http://www.amstat.org/publications/jse/v18n3/RicciData.csv))

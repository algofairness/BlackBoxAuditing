import os

datasets_dir = os.path.dirname(__file__)

preloaded = {
   "adult":    {"filepath": datasets_dir+"/adult.csv",
                "testdata": datasets_dir+"/adult.test.csv",
                "correct_types": [int, str, int, str, int, str, str, str,
                                  str,str, int, int, int, str, str],
                "train_percentage": None,
                "response_header": "income-per-year",
                "features_to_ignore": []},

   "diabetes": {"filepath": datasets_dir+"/pima-indians-diabetes.csv",
                "testdata": None,
                "correct_types": [int, float, float, float, float,
                                  float, float, int, str],
                "train_percentage": 1.0/2.0,
                "response_header": "Class",
                "features_to_ignore": []},

   "ricci":    {"filepath": datasets_dir+"/RicciDataMod.csv",
                "testdata": None,
                "correct_types": [str,float,int,str,float,str],
                "train_percentage": 1.0/2.0,
                "response_header": "Class",
                "features_to_ignore":[]},

   "german":   {"filepath": datasets_dir+"/german_categorical.csv",
                "testdata": None,
                "correct_types": [str, int, str, str, int, str, str, int, str, str, int,
                                  str, int, str, str, str, int, str, int, str, str, str],
                "train_percentage": 2.0/3.0,
                "response_header": "class",
                "features_to_ignore": ["age"]},

   "glass":    {"filepath": datasets_dir+"/glass.csv",
                "testdata": None,
                "correct_types": [int, float, float, float, float, float, float, float,
                                  float, float, str],
                "train_percentage": 1.0/2.0,
                "response_header": "type of glass",
                "features_to_ignore": []},

   "sample":   {"filepath": datasets_dir+"/sample.csv",
                "testdata": None,
                "correct_types": [int, int, int, int, float, str],
                "train_percentage":2.0/3.0,
                "response_header": "Outcome",
                "features_to_ignore": []},

   "DRP":      {"filepath": "test_data/DRP_nature_train.arff",
                "testdata": "test_data/DRP_nature_test.arff",
                "correct_types": [float]*2+[str,float,str]+[float]*162+[str]*58+[float]*48+[str],
                "train_percentage": 2.0/3.0,
                "response_header": "outcome",
                "features_to_ignore": []}

  }

import os
import subprocess

def test():
  here = os.path.abspath(os.path.dirname(__file__))
  os.chdir(here)
  output = subprocess.check_output("./run_test_suite.sh")
  print output

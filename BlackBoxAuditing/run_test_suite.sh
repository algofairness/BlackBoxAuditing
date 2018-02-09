#!/usr/bin/env bash

# Run this file with bash to run all Python files in this directory and in sub-directories.
# Note: excludes "__init__.py" files, "Abstract" files, and the "main.py" file.

# To implement a test, use the following format in the file-to-test:
#
# if __name__=="__main__": test()
# def test():
#   ...
#

# Add the current directory to the PYTHONPATH so imports start at the project root.
export PYTHONPATH="${PYTHONPATH}:`pwd`"
# specify the hash seed for reproducibility (only necessary for python3)
export PYTHONHASHSEED=1
echo "#########################################################################"
echo "### Running all *.py files now. #########################################"
echo "### No tests should be False nor should there be Traceback exceptions. ##"
echo "#########################################################################"

# Loop largely based on: http://stackoverflow.com/questions/15065010/how-to-perform-a-for-each-file-loop-by-using-find-in-shell-bash
find . -type f -iname "*.py" -print0 | while IFS= read -r -d $'\0' line; do
  if [[ ! $line =~ .*__init__.py ]]; then
    if [[ ! $line =~ .*Abstract.+.py ]]; then
      if [[ ! $line =~ ./BlackBoxAuditor.py ]]; then
        if [[ ! $line =~ ./histogram_maker.py ]]; then
          if [[ ! $line =~ ./disparate_impact_evaluator.py ]]; then
            if [[ ! $line =~ ./make_graphs.py ]]; then
              if [[ ! $line =~ ./find_contexts/extract_influence_scores.py ]]; then
                if [[ ! $line =~ ./find_contexts/find_cn2_rules.py ]]; then
                  if [[ ! $line =~ ./repair.py ]]; then
                    if [[ ! $line =~ ./setup.py ]]; then
                      if [[ ! $line =~ ./MANIFEST.in ]]; then
                        echo "________________________________"
                        echo "Running tests for: $line"
                        python3 "$line" | grep --color -E '^|False$' # Highlight "False" tests.
                      fi
                    fi
                  fi
                fi
              fi
            fi
          fi
        fi
      fi
    fi
  fi
done


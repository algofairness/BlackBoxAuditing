# Run this file with bash to run all Python files in this directory and in sub-directories.
# Note: excludes __init__.py files.

# To implement a test, use the following format in the file-to-test:
#
# if __name__=="__main__": test()
# def test():
#   ...
#

echo "Running all *.py files now."
echo "No tests should be False nor should there be Traceback exceptions."
echo "_______________________________________"
# Loop largely based on: http://stackoverflow.com/questions/15065010/how-to-perform-a-for-each-file-loop-by-using-find-in-shell-bash
find . -type f -iname "*.py" -print0 | while IFS= read -r -d $'\0' line; do
  if [[ ! $line =~ .*__init__.py ]]; then
    echo "Running tests for: $line"
    python "$line"
    echo "________________________________"
  fi
done


# Largely taken from: http://stackoverflow.com/questions/15065010/how-to-perform-a-for-each-file-loop-by-using-find-in-shell-bash
find . -type f -iname "*.py" -print0 | while IFS= read -r -d $'\0' line; do
  python "$line"
done


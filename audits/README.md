This directory will contain output files for GFA audits.
Each file should contain the following contents...

  GFA Audit for <FEATURE>
  repair level: confusion table for audit
  repair level': confusion table for audit
  repair level'': confusion table for audit
  ...

Each confusion table should be represented as a dictionary in the following format...

  {"actual-1":{"guess-1":occurrences, "guess-2":occurrences, ...}
   "actual-2":{"guess-1":occurrences, "guess-2":occurrences, ...}}

For example, if a model had two possible outcomes (A and B) for 1000 data points and guessed correctly 9/10 times, we might see a confusion table like this...

  {A:{A:450, B:50}, B:{A:50, B:450}}



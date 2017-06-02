import csv
from repair_kdd import setup_and_call_repair, perform_repair, repair_type
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--audit', dest='audit', default=False, action='store_true')
args = parser.parse_args()

def repair_script_test():
    outfile ="kdd/RicciResults.current.csv"
    infile = "kdd/RicciDataMod.csv"
    identifier_col_names = ["Position"]
    protected_col_names = ["Race"]
    stratify_col_names = ["Race"]
    repair_values = [1.0]
    requested_repair_type = repair_type.COMBINATORIAL

    for repair_amount in repair_values:
        repaired_data = setup_and_call_repair(infile, outfile, identifier_col_names, protected_col_names,
                                                stratify_col_names, repair_amount, requested_repair_type)
        if not args.audit:
            correct_data = "kdd/RicciResults.correct.csv"
        else:
            correct_data = "kdd/RicciRepaired1.0.audits.csv"

        reader1 = csv.reader(open(repaired_data, 'rb'))
        reader2 = csv.reader(open(correct_data, 'rb'))

        # Skip the header 
        reader1.next()
        reader2.next()
        passed = True
        for i, repaired_row in enumerate(reader1):
            correct_row = reader2.next()
            # change strings to floats to compare the two
            repaired = [float(x) for x in repaired_row]
            correct = [float(x) for x in correct_row]
            if repaired != correct:
                print "Oops Repair Script Incorrect!", i
                print "Got:      ", repaired
                print "Expected: ", correct
                passed = False
        if passed:
                print "Test Passed"

def test():
    repair_script_test()

if __name__ == "__main__": test()

import csv

f1 = 'repair_tests/output/repairtest.csv'
f2 = 'repair_tests/TrueKDDRepairWhite.csv'

with open(f1, 'r') as t1, open(f2, 'r') as t2:
    fileone = t1.readlines()
    filetwo = t2.readlines()

with open('repair_tests/update.csv', 'w') as outFile:
    for line in filetwo:
        if line not in fileone:
            outFile.write(line)
            #pass

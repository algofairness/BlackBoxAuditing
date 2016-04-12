import csv 
dict_list_of_dicts = {}
count = 1
with open('Georgia_cleaned.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	id = 1
	dict_list_of_dicts[count] = []
	for row in reader:
		if id >= 1000:
			id = 1
			count += 1
			dict_list_of_dicts[count] = []
		dict={}
		dict['id'] = id
		dict['street_address'] = row['STREET NUMBER'] + " " + row['STREET']
		dict['city'] = row['CITY']
		dict['state'] = row['STATE']
		dict['zip'] = row['ZIP CODE']
		dict_list_of_dicts[count].append(dict)
		id += 1
i = 1			
while i <= count:
	with open('Georgia_addresses{}.csv'.format(str(i)), 'w') as csvfile:
	    fieldnames = ['id','street_address', 'city', 'state','zip']
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

	    #writer.writeheader()
	    for dict in dict_list_of_dicts[i]:
	   		writer.writerow(dict)
	i += 1
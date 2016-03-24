import csv 
dict_of_dicts = {}
with open('block_groups.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		dict={}
		dict['rownum']=row['id']
		dict['GEOID10_BlkGrp']=row['GEOID10_BlkGrp']
		dict['GEOID10_Tract']=row['GEOID10_Tract']
		dict['geo_code_precision']=row['geo_code_precision']
		dict_of_dicts[row['id']] = dict

with open('Georgia_cleaned.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		dict=dict_of_dicts[row['RowNum']]
		dict['name1']=row['NAME']
		dict['name2']=''
		dict['ZCTA5']=row['ZIP CODE']
		
with open('georgia_bisg.csv', 'w') as csvfile:
	    fieldnames = ['rownum','name1', 'name2', 'GEOID10_BlkGrp', 'GEOID10_Tract', 'ZCTA5', 'geo_code_precision']
	    writer = csv.writer(csvfile)
	    writer.writerow(fieldnames)
	    for key,dict in dict_of_dicts.items():
	    	writer.writerow([dict[fieldname] for fieldname in fieldnames])

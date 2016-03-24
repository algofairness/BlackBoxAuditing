import csv 
dict_list_of_dicts = {}
count0=0
count1=0
for i in range(1,22):
	dict_list_of_dicts[i] = []
	with open('GeocodeResults ({}).csv'.format(i)) as csvfile:
		reader = csv.DictReader(csvfile,fieldnames=['id','1','match','3','4','5','6','7','state','county','tract','block'])
		for row in reader:
			if row['match'] == "Match":
				count0+=1
				block_group = row['state'] + row['county'] + row['tract'] + row['block'][0]
				tract = row['state'] + row['county'] + row['tract']
				precision = "USAStreetAddr"
			else: 
				count1+=1
				block_group = ""
				tract = ""
				precision = "USAZipcode"
			dict={}
			dict['id'] = str(int(row['id'])+(999*(i-1)))
			dict['GEOID10_BlkGrp'] = block_group
			dict['GEOID10_Tract'] = tract
			dict['geo_code_precision'] = precision
			dict_list_of_dicts[i].append(dict)	
print float(count1)/(count0+count1)
print count1+count0
with open('block_groups.csv', 'w') as csvfile:
	fieldnames = ['id','GEOID10_BlkGrp', 'GEOID10_Tract', 'geo_code_precision']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for i in range(1,22):
		for dict in dict_list_of_dicts[i]:
   			writer.writerow(dict)
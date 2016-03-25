import csv
import math
dict_of_dicts={}
with open('georgia_bisg_output.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		list = [(row['pr_white'], 'White'),(row['pr_black'], 'Black'),(row['pr_hispanic'], 'Hispanic'),(row['pr_api'], 'Asian or Pacific Islander'),(row['pr_aian'], 'American Indian or Alaskan Native'),(row['pr_mult_other'], 'Other')]
		tuple = max(list,key=lambda item:item[0])
		pred_race = tuple[1]
		black_zip = '1'
		black_name = '1'
		dict={}
		dict['pred_race']= pred_race
		dict['black_zip']= black_zip
		dict['black_name'] = black_name
		dict_of_dicts[row['rownum']] = dict

with open('Georgia_cleaned.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		try: 
			dict_of_dicts[row['RowNum']]
			dict=dict_of_dicts[row['RowNum']]
			dict['race']=row['RACE']
			dict['sex']=row['SEX']
			dict['yearofbirth']=row['YEAR OF BIRTH']
			incarcerated =  str(row['INCARCERATED'] )[0]
			absconder = str(row['ABSCONDER'])[0]
			predator = str(row['PREDATOR'])[0]
			dict['incarcerated']=incarcerated
			dict['absconder'] = absconder
			dict['predator'] = predator
		except:
			continue
		
with open('Georgia_confusionmatrix_final.csv', 'w') as csvfile:
	    fieldnames = ['pred_race','race','black_zip','black_name','sex','yearofbirth','incarcerated','absconder','predator']
	    writer = csv.writer(csvfile)
	    writer.writerow(fieldnames)
	    for key,dict in dict_of_dicts.items():
	    	writer.writerow([dict[fieldname] for fieldname in fieldnames])

with open('Georgia_cleaned.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		try: 
			dict_of_dicts[row['RowNum']]
			dict=dict_of_dicts[row['RowNum']]
			dict['height'] = row['HEIGHT']
			dict['weight'] = row['WEIGHT']
			dict['haircolor'] = row['HAIR COLOR']
			dict['eyecolor'] = row['EYE COLOR']
			dict['zipcode'] = row['ZIP CODE']
			dict['registrationdate'] = row["REGISTRATION DATE"]
			dict['crime'] = row['CRIME']
			dict['convictiondate'] = row['CONVICTION DATE']
			dict['convictionstate'] = row['CONVICTION STATE']
		except:
			continue
		
with open('../test_data/Georgia_truerace.csv', 'w') as csvfile:
	    fieldnames = ['race','sex','yearofbirth','height','weight','haircolor','eyecolor','zipcode','registrationdate','crime','convictiondate','convictionstate','incarcerated','absconder','predator']
	    writer = csv.writer(csvfile)
	    writer.writerow(fieldnames)
	    for key,dict in dict_of_dicts.items():
	    	writer.writerow([dict[fieldname] for fieldname in fieldnames])
with open('../test_data/Georgia_predrace.csv', 'w') as csvfile:
	    fieldnames = ['pred_race','sex','yearofbirth','height','weight','haircolor','eyecolor','zipcode','registrationdate','crime','convictiondate','convictionstate','incarcerated','absconder','predator']
	    writer = csv.writer(csvfile)
	    writer.writerow(fieldnames)
	    for key,dict in dict_of_dicts.items():
	    	writer.writerow([dict[fieldname] for fieldname in fieldnames])
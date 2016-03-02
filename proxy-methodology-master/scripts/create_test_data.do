* This program creates a fictitious sample data set based on a random sample
* of records from the public use census surname list and census geography files.
* Because areas spanned by ZIP codes are not necessarily nested within census geography (like tract or block group)
* the ZIP code level demographic file does not contain tract or block group identifiers.
* In constructing this sample data set, created solely for the purpose of illustrating how to
* set up the proxy building code sequence, we select a random list of ZIP codes, which will
* likely be unrelated to the tract or block groups to which they will be merged.  This
* fictitious sample data cannot be used to test the accuracy of the proxy.

set more off
set type double

* Read in surname data and take a random draw of 100 individuals for applicant last name.
insheet using "../input_files/app_c.csv", comma clear
bysort name: assert _n==_N
sort name

set seed 1234
gen draw = runiform()
sort draw
keep if _n <= 100

gen rownum = _n
rename name name1
keep rownum name1
tempfile t1
save `t1'

* Read in surname data and take a random draw of 25 individuals for coapplicant last name.
insheet using "../input_files/app_c.csv", comma clear
bysort name: assert _n==_N
sort name

set seed 5678
gen draw = runiform()
sort draw
keep if _n <= 25

gen rownum = _n
rename name name2
keep rownum name2
tempfile t2
save `t2'

* Read in geography data from census geography files.

* Block groups are nested within tracts, so merge tract and block group codes.
use "../input_files/tract_over18_race_dec10", clear 
keep GEOID10_Tract State_FIPS10 County_FIPS10 Tract_FIPS10
bysort State_FIPS10 County_FIPS10 Tract_FIPS10: assert _n == _N

merge 1:m State_FIPS10 County_FIPS10 Tract_FIPS10 using "../input_files/blkgrp_over18_race_dec10", keepusing(GEOID10_BlkGrp State_FIPS10 County_FIPS10 Tract_FIPS10 BlkGrp_FIPS10)
bysort State_FIPS10 County_FIPS10 Tract_FIPS10 BlkGrp_FIPS10: assert _n ==_N

* Remove Puerto Rico 
drop if State_FIPS10 == "72"
    
set seed 91011
gen draw = runiform()
sort draw
keep if _n <= 100

gen rownum = _n
keep rownum GEOID10_Tract GEOID10_BlkGrp
tempfile t3
save `t3'

* ZIP code is not strictly nested within census geography.
* Draw a random sample of ZIP codes, which likely not correspond to the tract and block groups above.
use "../input_files/zip_over18_race_dec10", clear 

* Remove Puerto Rico
drop if inlist(substr(ZCTA5,1,3),"006","007","008","009")

set seed 121314
gen draw = runiform()
sort draw
keep if _n <= 100

gen rownum = _n
keep rownum ZCTA5
tempfile t4
save `t4'

use `t1', clear
merge 1:1 rownum using `t2'
assert _m == 3 | _m == 1
drop _m
merge 1:1 rownum using `t3'
assert _m == 3
drop _m
merge 1:1 rownum using `t4'
assert _m == 3
drop _m

* Randomly assign a ficitious precision value for geocoding
set seed 151617
gen draw = runiform()
gen geo_code_precision = ""
replace geo_code_precision = "USAStreetAddr" if draw < 0.90 & mi(geo_code_precision)
replace geo_code_precision = "USAStreetName" if draw < 0.95 & mi(geo_code_precision)
replace geo_code_precision = "USAZIP4" if draw < 0.97 & mi(geo_code_precision)
replace geo_code_precision = "USAZipcode" if draw <= 100 & mi(geo_code_precision)
assert !mi(geo_code_precision)
drop draw
tab geo_code_precision, m

* Convert geography codes and ZIP code to numeric.
destring GEOID10_Tract GEOID10_BlkGrp ZCTA5, replace

keep rownum name1 name2 GEOID10_Tract GEOID10_BlkGrp ZCTA5 geo_code_precision 
order rownum name1 name2 GEOID10_Tract GEOID10_BlkGrp ZCTA5 geo_code_precision 

save "../output/fictitious_sample_data", replace

* END





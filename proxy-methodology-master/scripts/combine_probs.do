* This program merges together the block group, tract, and ZIP code based BISG proxies
* and chooses the most precise proxy given the precision of geocoding.
*
* Input arguments:
*
* matchvars - unique record identifier
* maindir - directory containing files with BISG proxies created by subroutine in geo_name_merge_all_entities_over18.do
* geodir - input directory that contains geocoded data
* geofile - institution specific geocoded data
* inst_name - string that is use to create file name for final output dataset

capture program drop combine_bisg
program define combine_bisg, byable(recall)
    version 11
    syntax [if] [in] [, matchvars(string) maindir(string) geodir(string) geofile(string) geoprecvar(string) inst_name(string)]

clear
 
* Merge together the three files containing BISG proxies for blkgrp, tract, or ZIP code.

* Read in BISG proxies based on block group.
use "`maindir'/`inst_name'_proxied_blkgrp18.dta"

* Merge in BISG proxies based on tract.
merge 1:1 `matchvars' using "`maindir'/`inst_name'_proxied_tract18.dta"
assert _m == 3
drop _m

* Merge in BISG proxies based on ZIP code.
merge 1:1 `matchvars' using "`maindir'/`inst_name'_proxied_zip18.dta"
assert _m == 3
drop _m

* Merge in file containing geocodes and keep the variable containing the geography precision code.
merge 1:1 `matchvars' using "`geodir'/`geofile'.dta", keepusing(`matchvars' `geoprecvar')
assert _m == 3
drop _m

* Create the final BISG proxy.
* For records geocoded to the street ("USAStreetName"), 9-digit ZIP code ("USAZIP4"), and 5-digit ZIP code ("USAZipcode"), use 5-digit ZIP code demographics.
* For records geocoded to the rooftop ("USAStreetAddr"), use first available: block group, tract, or 5-digit ZIP code demographics.
* 
* Precision codes are those genearted by ArcGIS. 
* The pr_ variables are the final BISG probabilities:
*
* white - non-Hispanic White
* black - non-Hispanic Black
* hispanic - Hispanic
* api - Asian/Pacific Islander
* aian - American Indian/Alaska Native
* mult_other - Multiracial/Other
*
* blkgrp18_pr_ is the BISG probability based on block group level demographics
* tract18_pr_ is the BISG probability based on tract level demographics
* zip18_pr_ is the BISG probabilitiy based on 5-digit ZIP code level demographics
*
* blkgrp18_geo_pr_ is the geography-only probability based on block group
* tract18_geo_pr_ is the geography-only probability based on tract
* zip18_geo_pr_ is the geography-only probability based on 5-digit ZIP code
* name_pr_ is the surname-only probability 
*
* pr_precision reflects the level of geographic detail associated with the selection of the demographics 

foreach q in blkgrp18 tract18 zip18 {
	egen sum_`q'_pr = rowtotal(`q'_pr_*)
	}

gen pr_precision = .
replace pr_precision = 2 if inlist(`geoprecvar',"USAStreetName","USAZIP4","USAZipcode") & !mi(sum_zip18_pr) & sum_zip18_pr > 0 & mi(pr_precision)
replace pr_precision = 3 if inlist(`geoprecvar',"USAStreetAddr") & !mi(sum_blkgrp18_pr) & sum_blkgrp18_pr > 0 & mi(pr_precision)
replace pr_precision = 4 if inlist(`geoprecvar',"USAStreetAddr") & !mi(sum_tract18_pr) & sum_tract18_pr > 0 & mi(pr_precision)
replace pr_precision = 5 if inlist(`geoprecvar',"USAStreetAddr") & !mi(sum_zip18_pr) & sum_zip18_pr > 0 & mi(pr_precision)
replace pr_precision = 1 if mi(pr_precision)

di in ye "Check that precision assigned to all observations"
assert !mi(pr_precision)

label define pr_precision 1 "NO FINAL PROB ASSIGNED" 2 "ZIP (not rooftop lat/long)" 3 "BLKGRP (has rooftop lat/long)" 4 "TRACT (has rooftop lat/long)" 5 "ZIP (has rooftop lat/long)"
label val pr_precision pr_precision

tab pr_precision, m
tab pr_precision `geoprecvar', m

foreach v in white black hispanic api aian mult_other {
    gen pr_`v'=.
    replace pr_`v'=zip18_pr_`v' if pr_precision == 2
    replace pr_`v'=blkgrp18_pr_`v' if pr_precision == 3
    replace pr_`v'=tract18_pr_`v' if pr_precision == 4
    replace pr_`v'=zip18_pr_`v' if pr_precision == 5
    }

* Check that final probabilities sum to 1.
egen check_pr = rowtotal(pr_white pr_black pr_aian pr_api pr_mult_other pr_hispanic)
di in ye "Checking final probabilities sum to 1"
assert check_pr == 0 if pr_precision == 1 
assert check_pr >= 0.99 & check_pr <= 1.01 if pr_precision > 1
drop check_pr sum_*

order `matchvars' `geoprecvar' pr_* blkgrp18_pr_* tract18_pr_* zip18_pr_* blkgrp18_geo_pr_* tract18_geo_pr_* zip18_geo_pr_* name_pr*
save  "`maindir'/`inst_name'_proxied_final.dta",replace   
 
end

* END




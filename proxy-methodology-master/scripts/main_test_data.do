* This Stata script executes a series of Stata scripts and subroutines that
* prepare input public use census geography and surname data
* and constructs the surname-only, geography-only, and BISG proxies for
* race and ethnicity.
*
* This file is set up to execute the proxy building code sequence on a set of 
* fictitious data constructed by create_test_data.do from the publicly available census surname
* list and geography data. It is provided to illustrate how the main.do
* is set up to run the proxy building code.

set more off
set trace off
set type double 
set mem 12g

* Identify the input directory that contains the individual or application level data containing name and geocodes.
local sourcedir = "../test_output"

* Identify the output directory for processing.
local outdir = "../test_output"

* Identify the location of the prepared input census files.
local censusdata = "../input_files/created"

* Run the script that prepares the analysis version of the census surname list,
* including the proportions of individuals by race and ethnicity by surname.
do "surname_creation_lower.do"

* Run the script that prepares the analysis version of the census geography data files.
do "create_attr_over18_all_geo_entities.do"

* Read in the file that defines the program "name_parse" that contains the name standardization routines and merges surname probabilities
* from the census surname list.
* See script for details on arguments that need to be supplied to the program.
do "surname_parser.do"
* Execute name_parse.
name_parse, matchvars(rownum) app_lname(name) coapp_lname(name) maindir(`outdir') readdir(`sourcedir') readfile(Georgia) censusdir(`censusdata') keepvars()

* Read in the file (for each level of geography) that defines the program "geo_parse" that merges the precalculated geographic 
* and name probabilities and generates the Bayesian probability and run program.
* See script for details on arguments that need to be supplied to the program.
do "geo_name_merger_all_entities_over18.do"
* Execute geo_parse to construct block group, tract, and ZIP code based BISG probabilities.
*geo_parse, matchvars(rownum) maindir(`outdir') readdir(`sourcedir') readfile(fictitious_sample_data) geodir(`sourcedir') geofile(Georgia) inst_name(test) censusdir(`censusdata') geo_ind_name(GEOID10_BlkGrp) geo_switch(blkgrp)
*geo_parse, matchvars(rownum) maindir(`outdir') readdir(`sourcedir') readfile(fictitious_sample_data) geodir(`sourcedir') geofile(Georgia) inst_name(test) censusdir(`censusdata') geo_ind_name(GEOID10_Tract) geo_switch(tract)
geo_parse, matchvars(rownum) maindir(`outdir') readdir(`sourcedir') readfile(Georgia) geodir(`sourcedir') geofile(Georgia) inst_name(test) censusdir(`censusdata') geo_ind_name(zipcode) geo_switch(zip)

merge 1:1 rownum using "../test_output/Georgia.dta"
assert _m == 3
drop _m
save ../test_output/Georgia_out, replace
gen pred_race = "Default"
replace pred_race = "WHITE" if zip18_geo_pr_white >= zip18_geo_pr_black & zip18_geo_pr_white >= zip18_geo_pr_aian & zip18_geo_pr_white >= zip18_geo_pr_api & zip18_geo_pr_white >= zip18_geo_pr_mult_other & zip18_geo_pr_white >= zip18_geo_pr_hispanic
replace pred_race = "BLACK" if zip18_geo_pr_black >= zip18_geo_pr_white & zip18_geo_pr_black >= zip18_geo_pr_aian & zip18_geo_pr_black >= zip18_geo_pr_api & zip18_geo_pr_black >= zip18_geo_pr_mult_other & zip18_geo_pr_black >= zip18_geo_pr_hispanic
replace pred_race = "ASIAN" if zip18_geo_pr_aian >= zip18_geo_pr_white & zip18_geo_pr_aian >= zip18_geo_pr_black & zip18_geo_pr_aian >= zip18_geo_pr_api & zip18_geo_pr_aian >= zip18_geo_pr_mult_other & zip18_geo_pr_aian >= zip18_geo_pr_hispanic
replace pred_race = "ASIAN PACIFIC ISLANDER" if zip18_geo_pr_api >= zip18_geo_pr_white & zip18_geo_pr_api >= zip18_geo_pr_black & zip18_geo_pr_api >= zip18_geo_pr_aian & zip18_geo_pr_api >= zip18_geo_pr_mult_other & zip18_geo_pr_api >= zip18_geo_pr_hispanic
replace pred_race = "OTHER/MULT" if zip18_geo_pr_mult_other >= zip18_geo_pr_white & zip18_geo_pr_mult_other >= zip18_geo_pr_black & zip18_geo_pr_mult_other >= zip18_geo_pr_aian & zip18_geo_pr_mult_other >= zip18_geo_pr_api & zip18_geo_pr_mult_other >= zip18_geo_pr_hispanic
replace pred_race = "HISPANIC" if zip18_geo_pr_hispanic >= zip18_geo_pr_white & zip18_geo_pr_hispanic >= zip18_geo_pr_black & zip18_geo_pr_hispanic >= zip18_geo_pr_aian & zip18_geo_pr_hispanic >= zip18_geo_pr_api & zip18_geo_pr_hispanic >= zip18_geo_pr_mult_other

gen black_zip = 0
replace black_zip = 1 if zip18_pr_black >= zip18_pr_white & zip18_pr_black >= zip18_pr_aian & zip18_pr_black >= zip18_pr_api & zip18_pr_black >= zip18_pr_mult_other & zip18_pr_black >= zip18_pr_hispanic

gen black_name = 0
replace black_name = 1 if name_pr_black >= name_pr_white & name_pr_black >= name_pr_aian & name_pr_black >= name_pr_api & name_pr_black >= name_pr_mult_other & name_pr_black >= name_pr_hispanic

*full data
outsheet black_zip black_name zip18_geo_pr_white zip18_geo_pr_black zip18_geo_pr_aian zip18_geo_pr_api zip18_geo_pr_mult_other zip18_geo_pr_hispanic rownum name_pr_hispanic name_pr_white name_pr_black name_pr_api name_pr_aian name_pr_mult_other zip18_pr_white zip18_pr_black zip18_pr_aian zip18_pr_api zip18_pr_hispanic zip18_pr_mult_other name sex race yearofbirth height weight haircolor eyecolor streetnumber street city state zipcode county registrationdate crime convictiondate convictionstate incarcerated predator absconder resverificationdate geo_code_precision pred_race using  ../test_output/Georgia_full.csv, comma nolabel replace
*true race 
outsheet race sex yearofbirth height weight haircolor eyecolor streetnumber street city state zipcode county registrationdate crime convictiondate convictionstate incarcerated absconder predator using  ../test_output/Georgia_truerace.csv, comma nolabel replace
*pred race
outsheet pred_race sex yearofbirth height weight haircolor eyecolor streetnumber street city state zipcode county registrationdate crime convictiondate convictionstate incarcerated absconder predator using  ../test_output/Georgia_predrace.csv, comma nolabel replace
*confusion matrix
outsheet race pred_race black_zip black_name sex yearofbirth incarcerated absconder predator using  ../test_output/Georgia_confusionmatrix.csv, comma nolabel replace


* Read in file that defines the program "combine_probs" that merges together the block group, tract, and zip based BISG proxies and
* chooses the most precise proxy given the precision of geocoding.
* See script for details on arguments that need to be supplied to the function.
*do "combine_probs.do"
* Execute combine_bisg.
*combine_bisg, matchvars(rownum) maindir(`outdir') geodir(`sourcedir') geofile(Georgia) geoprecvar(geo_code_precision) inst_name(test)





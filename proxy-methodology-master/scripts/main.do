* This Stata script executes a series of Stata scripts and subroutines that
* prepare and input public use census geography and surname data
* and constructs the surname-only, geography-only, and BISG proxies for
* race and ethnicity.
*
* Users must define a number of parameters, including file paths and arguments for
* subroutines. The scripts that define the subroutines also identify and describe arguments required.
* 
* Users must supply their own application- or individual-level data and any geocoding of 
* those data must occur prior to the execution of this script sequence: this code
* assumes that the input application- or individual-level data are already geocoded with
* census block group, census tract, and 5-digit ZIP code.

set more off
set trace off
set type double 
set mem 12g

* Identify the input directory that contains the individual or application level data containing name and geocodes.
local sourcedir = 

* Identify the output directory for processing.
local outdir = 

* Identify the location of the prepared input census files.
local censusdata = 

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
name_parse, matchvars() app_lname() coapp_lname() maindir() readdir() readfile() censusdir() keepvars()

* Read in the file (for each level of geography) that defines the program "geo_parse" that merges the precalculated geographic 
* and name probabilities and generates the Bayesian probability.
* See script for details on arguments that need to be supplied to the program.
do "geo_name_merger_all_entities_over18.do"
* Execute geo_parse to construct block group, tract, and ZIP code based BISG probabilities:
* Block group BISG:
geo_parse, matchvars() maindir() readdir() readfile() geodir() geofile() inst_name() censusdir() geo_ind_name() geo_switch(blkgrp)
* Tract BISG:
geo_parse, matchvars() maindir() readdir() readfile() geodir() geofile() inst_name() censusdir() geo_ind_name() geo_switch(tract)
* ZIP code BISG:
geo_parse, matchvars() maindir() readdir() readfile() geodir() geofile() inst_name() censusdir() geo_ind_name() geo_switch(zip)

* Read in file that defines the program "combine_probs" that merges together the block group, tract, and ZIP code based BISG proxies and 
* chooses the most precise proxy given the precision of geocoding.
* See script for details on arguments that need to be supplied to the function.
do "combine_probs.do"
* Execute combine_bisg.
combine_bisg, matchvars() maindir() geodir() geofile() geoprecvar() inst_name()





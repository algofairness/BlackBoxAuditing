* This script creates the master surname list from the census surname file,
* including the proportions of individuals by race and ethnicity by surname.

clear all

set more off
set type double

* Input files are included in input_files subfolder.
insheet using "../input_files/app_c.csv", comma clear

replace name = trim(proper(name))

* Formats the values in the Census data as proportions.
foreach k in white black api aian 2prace hispanic {

destring pct`k', force replace
replace pct`k' = pct`k' / 100
}

gen countmiss = (pctwhite == .) + (pctblack == .) + (pctapi == .) + (pctaian == .) + (pct2prace == .) + (pcthispanic == .)
egen remaining = rowtotal(pctblack pctwhite pctapi pctaian pct2prace pcthispanic)
replace remaining = count * (1 - remaining)

foreach k in white black api aian 2prace hispanic {

replace pct`k' = remaining / (countmiss * count) if pct`k' == .
}

replace name = lower(name)

save "../input_files/created/census_surnames_lower.dta", replace

exit

*END

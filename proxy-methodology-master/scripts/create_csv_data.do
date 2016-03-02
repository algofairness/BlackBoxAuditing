clear
insheet using ../test_output/Georgia_cleaned.csv, clear
drop if length(zipcode) !=5
destring zipcode, replace
gen rownum = _n
gen geo_code_precision = "USAZipcode"
save ../test_output/Georgia, replace

insheet using ../test_output/georgia_bisg.csv, clear
drop name2
gen name2=""
drop if zcta5 == ""
drop if zcta5 == "0"
destring zcta5, generate(ZCTA5) force
gen GEOID10_Tract = geoid10_tract
gen GEOID10_BlkGrp = geoid10_blkgrp
drop zcta5  geoid10_tract geoid10_blkgrp
save ../test_output/fictitious_sample_data, replace

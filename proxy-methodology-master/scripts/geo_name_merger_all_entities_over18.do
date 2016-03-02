* This program is called from an external script and merges the name probabilities
* and census geography data to generate the Bayesian updated probability.
*
* Input arguments:
*
* matchvars() - unique record identifier
* maindir() - output directory
* readdir() - directory containing individual or application data
* readfile() - individual or application data file 
* geodir() - input directory that contains geocoded data
* geofile() - institution specific geocoded data
* inst_name() - string that is use to create file name for final output dataset
* censusdir() - directory containing prepared input census geography and surname data
* geo_ind_name() - string that identifies the name of the geographic indicator in the loan or individual level analysis data (the program will change the name of the fips variable in the geocoded data to match this in order to merge)
* geo_switch() - string that identifies level of geography used taking the following values: blkgrp, tract, or zip (same values as used in geo creator)

capture program drop geo_parse
program define geo_parse, byable(recall)
    version 11
    syntax [if] [in] [, matchvars(string) maindir(string) readdir(string) readfile(string) geodir(string) geofile(string) censusdir(string) inst_name(string) geo_ind_name(string) geo_switch(string)]

clear
#delimit cr

foreach file in `geo_switch'{

    use "`geodir'/`geofile'.dta", clear

    merge 1:1 `matchvars' using "`readdir'/`readfile'.dta", keep(match using) update replace nogen

    save "`maindir'/`inst_name'_proxied.dta", replace

    use "`censusdir'/`file'_attr_over18.dta", clear

    destring GeoInd, replace

    rename GeoInd `geo_ind_name'

    merge 1:m `geo_ind_name' using "`maindir'/`inst_name'_proxied.dta", keep(match using) update replace nogen

    * Now incorporate name-based probabilities.

    merge 1:1 `matchvars' using "`maindir'/proxy_name.dta", keep(match master) nogen

    cap renpfix post_pr name_pr
    cap rename name_pr_2prace name_pr_mult_other

* Use Bayesian updating to combine name and geo probabilities.
* Follow the method and notation in Elliott et al. (2009).
* u_white=P(white|name)*P(this tract|white), and so on for other races.
    foreach race in white black aian api mult_other hispanic{
        gen u_`race' = name_pr_`race' * here_given_`race'
    }


    foreach race in white black aian api hispanic mult_other{
        gen pr_`race' = u_`race' / (u_white + u_black + u_aian + u_api + u_hispanic + u_mult_other)
    }

    drop u_* here* 

    cap drop prtotal
    egen prtotal = rowtotal(pr_white pr_black pr_aian pr_api pr_hispanic pr_mult_other)

    foreach race in white black aian api hispanic mult_other{
        replace pr_`race' = . if prtotal < .99
        *.99 chosen as these should sum to approximately 1, give or take rounding error.
    }

    drop prtotal

di in ye "Start assertions"
* Assertions:
* 1. All probabilities should be between 0 and 1.
    foreach race in white black aian api mult_other hispanic{
	di in ye "Checking name_pr_`race'"
        assert mi(name_pr_`race') | (name_pr_`race' >= 0 & name_pr_`race' <= 1) 
	di in ye "Checking geo_pr_`race'"
        assert mi(geo_pr_`race') | (geo_pr_`race' >= 0 & geo_pr_`race' <= 1)
	di in ye "Checking pr_`race'"
        assert mi(pr_`race') | (pr_`race' >= 0 & pr_`race' <= 1)
    }

* 2. Race probabilities should sum to at least 1.
    egen check_name = rowtotal(name_pr_white name_pr_black name_pr_aian name_pr_api name_pr_mult_other name_pr_hispanic)
    egen check_geo = rowtotal(geo_pr_white geo_pr_black geo_pr_aian geo_pr_api geo_pr_mult_other geo_pr_hispanic)
    egen check_pr = rowtotal(pr_white pr_black pr_aian pr_api pr_mult_other pr_hispanic)
    
    foreach type in name geo pr {
	di in ye "Checking sum of probabilities for `type'"
	assert check_`type' == 0 | (check_`type' >= 0.99) & (check_`type' <= 1.01)
	}
    
di in ye "End assertions"

* Rename BISG proxy variable to reflect geography used.
    foreach x in pr_white pr_black pr_aian pr_api pr_hispanic pr_mult_other geo_pr_white geo_pr_black geo_pr_aian geo_pr_api geo_pr_hispanic geo_pr_mult_other {
			rename `x' `geo_switch'18_`x'
    }
    
    keep `matchvars' `geo_switch'18_* name_pr*
    
    save "`maindir'/`inst_name'_proxied_`geo_switch'18.dta", replace
    
* Remove intermediate files.
    erase "`maindir'/`inst_name'_proxied.dta"

}

end

*END




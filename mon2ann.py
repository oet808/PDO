#!/usr/bin/python
###############################################################################
# Script that calls CDO
# linux command to calculate annual mean
# This is the unweighted mean (Jan, Feb, Mar, Apr hav same weight)
# IMPORTANT: THE CLENS monthly mean data have a time axis shifted 
# by one month! Feb in year i is the monthly mean of January year i
# Dec is Nov mean, and Jan year i+1 is the average of Dec year i!
###############################################################################

import os
#import sys
#sys.path.append("./modules")
from clens import *

def calc_ann_mean(scen,run,v):
    """calculates annual mean from monthly mean data using CDO.
    
    Input variables:
        scen,run,v are strings indicating the scenario, 
        ensemble member run, and the variable name.
        These variables are used to form the netcdf file names
        that are processed with cdo.
    """
    app="ann" # app is used in the output file name
    cesmscen=TRANSLATE[scen]['scen']
    cesmtime=TRANSLATE[scen]['time']
    infile=MODEL+"_"+cesmscen+"_"+v+"_"+cesmtime+"_"+run+".nc"
    # Input path and output path are the same 
    # for input files that are itself not the 
    # original data files
    outfile=MODEL+"_"+cesmscen+"_"+v+"_"+cesmtime+"_"+run+\
    "_"+app+".nc" 
    if CORRECT_ANN_CALENDAR:
        first_year=str(TRANSLATE[scen]['first_year'])
        os.system("rm buffer.nc buffer2.nc")
        cdo="cdo -v -timselmean,12 "+OUTPATH+infile+" buffer.nc"
        print(cdo)
        os.system(cdo)
        print("use cdo to overwrite time dimension / correct the calendar")
        cdo="cdo -v -settaxis,"+first_year+"-01-01,00:00:00,365day buffer.nc buffer2.nc\n"
        cdo=cdo+"cdo  -setcalendar,standard buffer2.nc "+OUTPATH+outfile
        print(cdo)
        os.system(cdo)

    else:
        cdo="cdo -v -timselmean,12 "+OUTPATH+infile\
        +" "+OUTPATH+outfile
        print(cdo)
        os.system(cdo)
    
    print ("Infile: "+infile)
    print ("Outfile:"+outfile)
    print ("Folder: "+OUTPATH)
    return


# Loop over scenarios
iscen=0
for scen in SCENARIOLIST:
    nmodel=0
    for run in ENSEMBLELIST:
        i=0
        for v in VARLIST:
            calc_ann_mean(scen,run,v)
            i+=1
    nmodel+=1
    print ("----------------------------------------------------------")
    print ("stats for simulations "+scen+" : variable "+v)
    print ("models: "+str(nmodel)+" variables: "+str(i))
    iscen+=1


 

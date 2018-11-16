#!/usr/bin/python
###############################################################################
# Script that calls CDO
# use cdo for a quick (FFT-basd lowpass filtering)
# The -detrend option is used by default (as recommended for FFT calculations)
# cdo  lowpass,0.25 -detrend CESM_BRCP85C5CNBDRD_SST_200601-208012_001_ann_ano_pdo_proj.nc test.nc
###############################################################################

import os
from numpy import  round
#import sys
#sys.path.append("./modules")
from clens import *


def lowpass(scen,run,v,f=0.1):
    """Low-pss filtering using CDO.

    Input variables:
        scen,run,v: strings indicating the scenario, 
        ensemble member run, and the variable name.
        These variables are used to form the netcdf file names
        that are processed with cdo.
        f: is the cut-off frequency (1/timesteps). Default is decadal low-pass filter (for annual data).
    """
    app="lp" # app is used in the output file name
    cesmscen=TRANSLATE[scen]['scen']
    cesmtime=TRANSLATE[scen]['time']
    infile=MODEL+"_"+cesmscen+"_"+v+"_"+cesmtime+"_"+run+"_ann_ano_pdo_proj.nc"
    # OUTPATH: Input path and output path are the same.
    outfile=MODEL+"_"+cesmscen+"_"+v+"_"+cesmtime+"_"+run+\
    "_ann_ano_pdo_proj_"+app+".nc" 
    cdo="cdo lowpass,"+str(round(f,4))+" -detrend "+\
        OUTPATH+infile+" "+OUTPATH+outfile
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
            lowpass(scen,run,v,f=LPCUTOFF)
            i+=1
    nmodel+=1
    print ("----------------------------------------------------------")
    print ("stats for simulations "+scen+" : variable "+v)
    print ("models: "+str(nmodel)+" variables: "+str(i))
    iscen+=1


 

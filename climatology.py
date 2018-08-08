#!/usr/bin/python
###############################################################################
# Script that calls CDO
# linux command to calculate the long-term climatology
# (from annual mean data)
###############################################################################

import os
#import sys
#sys.path.append("./modules")
from clens import *

def calc_clim(scen,run,v,startyr,endyr):
    """Calculates annual mean from monthly mean data using CDO.
    
    Input variables:
        scen,run,v: strings indicating the scenario, 
        ensemble member run, and the variable name.
        These variables are used to form the netcdf file names
        that are processed with cdo.
        startyr, endyr: integer numbers for the first and last year
    """
    app="clim" # app is used in the output file name
    cesmscen=TRANSLATE[scen]['scen']
    cesmtime=TRANSLATE[scen]['time']
    infile=MODEL+"_"+cesmscen+"_"+v+"_"+cesmtime+"_"+run+"_ann.nc"
    # OUTPATH: Input path and output path are the same.
    outfile=MODEL+"_"+cesmscen+"_"+v+"_"+cesmtime+"_"+run+\
    "_ann_"+app+".nc" 
    cdo="cdo -v timmean -selyear,"+str(START)+"/"+str(END)+" "+\
    OUTPATH+infile+" "+OUTPATH+outfile
    print(cdo)
    os.system(cdo)
    print ("Infile: "+infile)
    print ("Outfile:"+outfile)
    print ("Folder: "+OUTPATH)
    return

# Loop over scenarios (historical only, usually)
iscen=0
for scen in ['historical']:
    nmodel=0
    for run in ENSEMBLELIST:
        i=0
        for v in VARLIST:
            calc_clim(scen,run,v,START,END)
            i+=1
    nmodel+=1
    print ("----------------------------------------------------------")
    print ("stats for simulations "+scen+" : variable "+v)
    print ("models: "+str(nmodel)+" variables: "+str(i))
    iscen+=1


 

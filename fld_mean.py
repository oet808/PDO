#!/usr/bin/python
###############################################################################
# Calculates the global mean using 'fldmean' operation in the CDO
# linux command (using annual mean data)
# The resulting netcdf file contains a single time series
# (but lon, lat coordinate dimensions will still exist in the output file)
###############################################################################

import os
#import sys
#sys.path.append("./modules")
from clens import *

def global_mean(scen,run,v):
    """Calculates the global mean (time series) using CDO.
    
    Input variables:
        scen,run,v: strings indicating the scenario, 
        ensemble member run, and the variable name.
        These variables are used to form the netcdf file names
        that are processed with cdo.
    """
    app="fldmean" # app is used in the output file name
    cesmscen=TRANSLATE[scen]['scen']
    cesmtime=TRANSLATE[scen]['time']
    infile=MODEL+"_"+cesmscen+"_"+v+"_"+cesmtime+"_"+run+"_ann_ano.nc"
    # OUTPATH: Input path and output path are the same.
    outfile=MODEL+"_"+cesmscen+"_"+v+"_"+cesmtime+"_"+run+\
    "_ann_"+app+".nc" 
    cdo="cdo  -v fldmean "+\
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
            global_mean(scen,run,v)
            i+=1
    nmodel+=1
    print ("----------------------------------------------------------")
    print ("stats for simulations "+scen+" : variable "+v)
    print ("models: "+str(nmodel)+" variables: "+str(i))
    iscen+=1


 

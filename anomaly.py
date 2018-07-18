#!/usr/bin/python
###############################################################################
# Script that calls CDO linux command to calculate 
# the annual anomalies with respect to the long-term climatology.
###############################################################################

import os
#import sys
#sys.path.append("./modules")
from clens_test import *

def calc_ano(scen,run,v,startyr,endyr):
    """Subtracts the climatology from the annual mean data using CDO.
    
    Input variables:
        scen,run,v: strings indicating the scenario, 
        ensemble member run, and the variable name.
        These variables are used to form the netcdf file names
        that are processed with cdo.
    """
    app="ano" # app is used in the output file name
    cesmscen=TRANSLATE[scen]['scen']
    cesmtime=TRANSLATE[scen]['time']
    infile=MODEL+"_"+cesmscen+"_"+v+"_"+cesmtime+"_"+run+"_ann.nc"
    infile_clim=MODEL+"_"+cesmscen+"_"+v+"_"+cesmtime+"_"+run+"_ann_clim.nc"
    # OUTPATH: Input path and output path are the same.
    outfile=MODEL+"_"+cesmscen+"_"+v+"_"+cesmtime+"_"+run+\
    "_ann_"+app+".nc" 
    cdo="cdo -v sub "+OUTPATH+infile+" "+OUTPATH+infile_clim+" "+\
    OUTPATH+outfile
    print(cdo)
    os.system(cdo)
    print ("Infile: "+infile)
    print ("Climatology: "+infile_clim)
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
            calc_ano(scen,run,v,START,END)
            i+=1
    nmodel+=1
    print ("----------------------------------------------------------")
    print ("stats for simulations "+scen+" : variable "+v)
    print ("models: "+str(nmodel)+" variables: "+str(i))
    iscen+=1


 

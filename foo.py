#!/usr/bin/python
###############################################################################
# Template script that calls CDO
# linux command to do some data processing with annual mean data
###############################################################################

import os
#import sys
#sys.path.append("./modules")
from clens_test import *

def calc_foo(scen,run,v):
    """Calculates something using CDO.
    
    Input variables:
        scen,run,v: strings indicating the scenario, 
        ensemble member run, and the variable name.
        These variables are used to form the netcdf file names
        that are processed with cdo.
    """
    app="foo" # app is used in the output file name
    cesmscen=TRANSLATE[scen]['scen']
    cesmtime=TRANSLATE[scen]['time']
    infile=MODEL+"_"+cesmscen+"_"+v+"_"+cesmtime+"_"+run+"_ann.nc"
    # OUTPATH: Input path and output path are the same.
    outfile=MODEL+"_"+cesmscen+"_"+v+"_"+cesmtime+"_"+run+\
    "_ann_"+app+".nc" 
    cdo="cdo foo "+\
    OUTPATH+infile+" "+OUTPATH+outfile
    print(cdo)
    #os.system(cdo)
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
            calc_foo(scen,run,v)
            i+=1
    nmodel+=1
    print ("----------------------------------------------------------")
    print ("stats for simulations "+scen+" : variable "+v)
    print ("models: "+str(nmodel)+" variables: "+str(i))
    iscen+=1


 

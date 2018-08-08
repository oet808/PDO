#!/usr/bin/python
###############################################################################
# Script that calls CDO
# linux command  to regrid 
# ocean model output to regular 2.5 x 2.5
# grid using bilinear interpolation
# Note: Updated variable naming: smallcaps 
# (all capital only for the 'contstant' variables from the module)
###############################################################################

def regrid(scen,run,v):
    """Regridding of netcdf data onto 2.5 x 2.5 lat-lon grid using CDO.
    
    Input variables:
        scen,run,v are strings indicating the scenario, 
        ensemble member run, and the variable name.
        These variables are used to form the netcdf file names
        that are processed with cdo.
    """
    cesmscen=TRANSLATE[scen]['scen']
    cesmtime=TRANSLATE[scen]['time']
    infile='b.e11.'+cesmscen+'.f09_g16.'+run+'.pop.h.'+v+\
    '.'+cesmtime+'.nc'
    source=DPATH+"/"+infile
    # extract variable
    os.system("rm buffer.nc") 
    cdo="cdo -selvar,"+v+" "+source+" buffer.nc"
    print(cdo)
    os.system(cdo)
    # remap to 2.5 x 2.5 NCEP grid
    outfile=MODEL+"_"+cesmscen+"_"+v+"_"+cesmtime+"_"+run+".nc"
    cdo="cdo -remapbil,"+OUTGRID+" buffer.nc "+OUTPATH+outfile
    print(cdo)
    os.system(cdo)
    # move 
    print ("infile: "+infile)
    print ("outfile: "+outfile)
    print ("Folder: "+OUTPATH)
    return 
   
import os
#import sys
#sys.path.append("./modules")
from clens import *
# Loop over scenarios
iscen=0
for scen in SCENARIOLIST:
    nmodel=0
    for run in ENSEMBLELIST:
        i=0
        for v in VARLIST:
            regrid(scen,run,v)
            i+=1
    nmodel+=1
    print ("----------------------------------------------------------")
    print ("stats for simulations "+scen+" : variable "+v)
    print ("models: "+str(nmodel)+" variables: "+str(i))
    iscen+=1
print ("done")



    

 

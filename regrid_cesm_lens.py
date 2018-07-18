#!/usr/bin/python
###############################################################################
# 2018-07-13 script that calls CDO
# linux command  to regrid 
# ocean model output to regular 2.5 x 2.5
# grid using bilinear interpolation
###############################################################################

import os

# label for the computer/ cluster used
WORKHOST="snow"

# Path to the directory with the source netcdf files
DPATH="/data/elisontimm_scr/DATA/CESM_LENS/" # must always end with '/'

# output data path
OUTPATH="/data/elisontimm_scr/DATA/CESM_LENS/DERIVED/" # must always end with '/'

# CMIP5 scenarios
#SCENARIOLIST=["historical","rcp85"]
SCENARIOLIST=["rcp85"]
# multi-model ensemble (like CMIP5) should use MODELLIST
# to iterate over model members
MODEL="CESM"

# only SST processed here, but can iterate over several variables in a file
VARLIST=["SST"]

# standard grid for all models
# This one is a 2.5 x 2.5 regular lon-lat grid
OUTGRID="/network/rit/lab/elisontimmlab_rit/DATA/NCEP/gridfile.nc"



###############################################################################
# CESM model specific variables
###############################################################################

ENSEMBLELIST=['001','002','003','004','005','006','007','008','009','010','011',\
            '012','013','014','015','016','017','018','019','020','021', \
            '022','023','024','025','026','027','028','029','030','031',\
            '032','033','034','035']

TRANSLATE={'historical':{'scen':'B20TRC5CNBDRD','time':'192001-200512'},\
                    'rcp85':{'scen':'BRCP85C5CNBDRD','time':'200601-208012'}}
TESTFILE="b.e11.B20TRC5CNBDRD.f09_g16.002.pop.h.SST.192001-200512.nc"


# LOOP OVER SCENARIOS
iscen=0
for SCENARIO in SCENARIOLIST:
    # LOOP OVER MODELS
    nmodel=0
    for RUN in ENSEMBLELIST:
        i=0
        for VAR in VARLIST:
            cesmscen=TRANSLATE[SCENARIO]['scen']
            cesmtime=TRANSLATE[SCENARIO]['time']
            INFILE='b.e11.'+cesmscen+'.f09_g16.002.pop.h.'+VAR+'.'+cesmtime+'.nc'
            SOURCE=DPATH+"/"+INFILE #SCENARIO+"/"+VAR+"/"+MODEL+"_"+RUN
            # extract variable
            os.system("rm buffer.nc") 
            cdo="cdo -selvar,"+VAR+" "+SOURCE+" buffer.nc"
            print(cdo)
            os.system(cdo)
            # remap to 2.5 x 2.5 NCEP grid
            outfile=MODEL+"_"+cesmscen+"_"+VAR+"_"+cesmtime+"_"+RUN+".nc"
            cdo="cdo -remapbil,"+OUTGRID+" buffer.nc "+OUTPATH+outfile
            print(cdo)
            os.system(cdo)
            # move 
            print (outfile)
            print ("Folder: "+OUTPATH)
            i+=1
    nmodel+=1
    print ("----------------------------------------------------------")
    print ("stats for simulations "+SCENARIO+" : variable "+VAR)
    print ("models: "+str(nmodel)+" variables: "+str(i))
    iscen+=1
print ("done")



    

 

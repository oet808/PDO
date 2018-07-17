#!/usr/bin/python
# 2018-07-13 script that calls CDO
# linux command  to regrid 
# ocean model output to regular 2.5 x 2.5
# grid using bilinear interpolation


import os

DPATH="/data/elisontimm_scr/DATA/CESM_LENS/"
WORKHOST="snow"

SCENARIOLIST=["historical","rcp85"]


SCENARIOLIST=["historical"]
#MODELLIST=["ACCESS1-0"]
MODEL="CESM"
# output data path
OUTPATH="/data/elisontimm_scr/DATA/CESM_LENS/DERIVED/"

VARLIST=["SST"]

# standard grid for all models
OUTGRID="/network/rit/lab/elisontimmlab_rit/DATA/NCEP/gridfile.nc"
iscen=-1





###############################
# CESM model specific variables
###############################
ENSEMBLELIST=['002']
TRANSLATE={'historical':{'scen':'B20TRC5CNBDRD','time':'192001-200512'},\
                    'rcp85':{'scen':'BRCP85C5CNBDRD','time':'200601-208012'}}
TESTFILE="b.e11.B20TRC5CNBDRD.f09_g16.002.pop.h.SST.192001-200512.nc"



# LOOP OVER SCENARIOS
for SCENARIO in SCENARIOLIST:
    iscen=iscen+1
    # LOOP OVER MODELS
    nmodel=0
    for RUN in ENSEMBLELIST:
        i=-1
        for VAR in VARLIST:
            cesmscen=TRANSLATE[SCENARIO]['scen']
            cesmtime=TRANSLATE[SCENARIO]['time']
            INFILE='b.e11.'+cesmscen+'.f09_g16.002.pop.h.'+VAR+'.'+cesmtime+'.nc'
            SOURCE=DPATH+"/"+INFILE #SCENARIO+"/"+VAR+"/"+MODEL+"_"+RUN
            # extract variable
            os.system("rm buffer,nc")
            cdo="cdo -selvar,"+VAR+" "+SOURCE+" buffer.nc"
            print cdo
            os.system(cdo)
           

            # remap to 2.5 x 2.5 NCEP grid
            cdo="cdo -remapbil,"+OUTGRID+" buffer.nc remap.nc"
            print cdo
            os.system(cdo)
            #
            outfile=MODEL+"_"+cesmscen+"_"+VAR+"_"+cesmtime+"_"+RUN+".nc"
            print (outfile)
            print ("Folder: "+OUTPATH)
            cmd="cp -p remap.nc "+OUTPATH+outfile
            os.system(cmd)
            os.system("rm buffer*.tmp buffer.nc remap.nc")
    nmodel+=1
    print ("----------------------------------------------------------")
    print ("stats for CMIP5 simulations "+SCENARIO+" : variable "+VAR)
    print ("models: "+str(nmodel))
print ("done")



    

 

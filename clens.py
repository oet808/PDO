###############################################################################
# Module that contains the CESM 
# Large Ensemble Simulation specifications
###############################################################################
"""Declarations of default variables for the CLENS ensemble. 
The test version does include a single scenario and single ensemble run.
"""

# Path to the directory with the source netcdf files
DPATH="/data/elisontimm_scr/DATA/CESM_LENS/" # must always end with '/'

# output data path
OUTPATH="/data/elisontimm_scr/DATA/CESM_LENS/DERIVED/" # must always end with '/'

# CMIP5 scenarios
SCENARIOLIST=["historical","rcp85"]

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

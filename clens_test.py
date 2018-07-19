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

ENSEMBLELIST=['001']




###############################################################################
# I use this dictionary to 'translate' the CMIP5 
# scenario labels to CLENS description of the scenarios
# this should help to write code for CLENS and CMIP5
# multi-model ensemble data processing. Currently
# this is dealing with the different file name conventions.
# Use of nested dictionaries allows for additional 
# 'translations'
###############################################################################
TRANSLATE={'historical':{'scen':'B20TRC5CNBDRD','time':'192001-200512',"first_year":1920},\
                    'rcp85':{'scen':'BRCP85C5CNBDRD','time':'200601-208012',"first_year":2006}}


###############################################################################
# Specific settings for data processing with CDO
###############################################################################

# APPLY time coordinate correction to when calculating 
# annual mean data from monthly data
CORRECT_ANN_CALENDAR=True 

# climatology: start and end years for the averaging
START=1975
END=2005

###############################################################################
# Define lat-lon region for spatially restricted analyses
###############################################################################
# For the PDO analysis (PCA and projection index)
REGION_PDO=(110.0,260.0,20.0,70.0)
# PCA (EOF) mode number for PDO (default value is first mode is PDO)
MODE_PDO=0 # first PCA mode should be PDO in models
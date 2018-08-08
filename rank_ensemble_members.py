###############################################################################
# Sort the ensemble members according the PDO index
# mean value for a chosen time period
# History:
# 
# 2018-08-08
#   validated RCP85 values with ferret (time series)
#   and visual check of SSTA pattern in ann_ano_resid files
###############################################################################
import numpy as np
import xarray
import matplotlib.pyplot as plt
import os
#import sys
#sys.append("./")
from clens import *
# need datetime for convenient handling of dates
import datetime as dt


def load_proj_time_series(scen,ens,v,mode):
    """Open a single netcdf file and extract a chosen projection index.

    Input: scen,ens,v are strings for the file names declaraition.
    mode: the selected projection index (mode number starting with 0)
    
    Return value:
    Numpy arrays with time and index data
    """
    cesmscen=TRANSLATE[scen]['scen']
    cesmtime=TRANSLATE[scen]['time']
    infile=MODEL+"_"+cesmscen+"_"+v+"_"+cesmtime+"_"+run+"_ann_ano_resid_pdo_proj_lp.nc"
    nc=xarray.open_dataset(OUTPATH+infile)
    time=nc['time'].data[:]
    index=nc['proj'].data[:,mode]
    nc.close()
    return time, index

def adjust_sign(scen,ens,v,mode):
    """The EOF pattern is checked for consistency with positve PDO phase sign convention.
    It checks for negative regional average in the central Pacific 32.5-42.5 N 130-180E.
    If positve value, then the function returns -1 else +1.
    
    Input variables: scen,ens,v are strings for the file name composition
    mode: chooses the PCA (EOF) mode number. Here mode=0 is the first PCA mode!
    (Note: The function loads the EOF pattern from the netcdf file.) 
    """
    cesmscen=TRANSLATE[scen]['scen']
    cesmtime=TRANSLATE[scen]['time']
    infile=MODEL+"_"+cesmscen+"_"+v+"_"+cesmtime+"_"+run+"_ann_ano_resid_eof.nc"
    nc=xarray.open_dataset(OUTPATH+infile)
    lon=nc['lon'].data
    lat=nc['lat'].data
    eof=nc['eof'].data[mode,:,:]
    is_lon=np.logical_and(lon>=130,lon<=180)
    is_lat=np.logical_and(lat>=32.5,lat<=42.5)
    buffer=eof[is_lat,:]
    res=buffer[:,is_lon]
    mean=np.nanmean(res)
    nc.close()
    return (-1*np.sign(mean)) # if SST anomaly negative then PDO index positive 

def convert_time(time):
    """convert numpy.datetime object into datetime object.
    
    Input: numpy array (1-dim) with numpy datetime data
    
    Return: numpy array with datetime objects)
    """
    dttime=[]
    for t in time:
        dttime.append(\
        dt.datetime.strptime(np.datetime_as_string(t)[0:10],"%Y-%m-%d"))
    return np.array(dttime)

###############################################################################
# Main
###############################################################################

# adjust variable name v used in filenames 
# ncvar is the internal netcdf variable name
v='SST'
ncvar='proj'

# plot time series yes/ no for true / false
is_plot= True


# Loop over scenarios                                                                                              
iscen=0                                                                                                           
SCENCOLORLIST={"historical":"blue","rcp85":"red"}
STARTYRLIST={"historical":1996,"rcp85":2026}
ENDYRLIST={"historical":2005,"rcp85":2035}

for scen in ['rcp85']:                                 
    nmodel=0      
    cesmscen=TRANSLATE[scen]['scen']      
    cesmtime=TRANSLATE[scen]['time']
    i=0
    # for eof sign check
    eofscen='historical'
    for run in ENSEMBLELIST:
        time,index=load_proj_time_series(scen,run,v,mode=MODE_PDO)
        # get length of time series to create array for the ensemble PDO indices
        if (i==0):
            ntime=len(time)
            nens=len(ENSEMBLELIST)
            pdomean=np.zeros(nens)
            help_sign=np.zeros(nens) # sign convention for PDO index help array
            buffer=np.zeros(shape=(ntime,nens))
        else:
            pass
        help_sign[i]=adjust_sign(eofscen,run,v,mode=MODE_PDO)
        buffer[:,i]=index*help_sign[i]
        if help_sign[i]<0:
            print(" ensemble # "+run)
            print("flip sign of EOF "+str(MODE_PDO)+" to match positive PDO phase pattern")
            print("invert prjection index series")
        # average over dynamical downscaling time interval
        dttime=convert_time(time)
        startyr=dt.datetime(STARTYRLIST[scen],1,1)
        endyr=dt.datetime(ENDYRLIST[scen],1,1)
        is_year=np.logical_and(dttime>=startyr,dttime<=endyr)
        pdomean[i]=np.mean(buffer[is_year,i])
        print(startyr,endyr,scen,run,pdomean[i],help_sign[i])
        i+=1
    iscen+=1
# Begin a new figure
if is_plot:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # only last scenario is stored in buffer
    i=0
    for run in ENSEMBLELIST:
        plt.plot(dttime,buffer[:,i])
        i+=1
    # adjust plot
    ax.set_xlabel("time")
    ax.set_ylabel("Projection index")
    ax.set_xlim([startyr,endyr])
    #ax.legend()
    fig.show()
###############################################################################
# Mean statistics for 2026-2035 and 1996-2005
# rank the Ensemble member according to PDO mean values
###############################################################################
print ("Ranking of ensemble members for scearion "+scen)
print (40*'-')
isort=np.argsort(pdomean)
k=0

fout=open(OUTPATH+cesmscen+"_ens_rank_pdo_index.csv",'w')
fout.write("rank,run,pdo\n")
k=1
for i in isort:
    print(k,ENSEMBLELIST[i],pdomean[i])
    fout.write(str(k)+" , "+ENSEMBLELIST[i]+" , "+str(np.round(pdomean[i],4))+"\n")
    k+=1
fout.close()
print ("Output for ensemble member ranking for PDO anoamlies:")
print (OUTPATH+cesmscen+"_ens_rank_pdo_index.csv")


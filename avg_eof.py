##############################################################################
# create ensemble average for the eof pattern
# (Default the leading PDO mode)
#
# The sign is determined by spatial correlation analysis
# between an ensemble member's eof and the eof from ensemble member 1
# (Use adjust_sign to flip sign of the ensemble mean EOF pattern
# to match the PDO positive phase).
##############################################################################
 
import numpy as np
import xarray
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as ccrs
import cartopy.feature as cfeature

#import sys
#sys.append("./")
from clens import *

def load_eof(scen,ens,v,mode):
    """ Load the EOF pattern from an ensemble member's PCA(EOF) analysis.
    
        NOTE: in this script the latitude and longitude are returned as 
        not as numpy arrays, but as the object types assigned by xarray

    Input parameter: 
    scen,ens,v are strings used to compose the file name
    mode: integer number that choses the EOF pattern mode number
    Return values:
    lat,lon: xarray object types from netcdf file 
    eof: numpy arrays (1-dim,1-dim, 2-dim) with latitude, longitude coordinates, and EOF pattern.
    
    """
    cesmscen=TRANSLATE[scen]['scen']
    cesmtime=TRANSLATE[scen]['time']
    infile=MODEL+"_"+cesmscen+"_"+v+"_"+cesmtime+"_"+run+"_ann_ano_resid_eof.nc"
    nc=xarray.open_dataset(OUTPATH+infile)
    eof=nc['eof'].data[mode,:,:]
    lat=nc['lat']# use .data[: in main program to access data as unmpy array]
    lon=nc['lon']# .data[:]
    nc.close()
    return lat,lon,eof

def adjust_sign(lat,lon,eof):
    """The EOF pattern is checked for consistency with positve PDO phase sign convention.
    It checks for negative regional average in the central Pacific 32.5-42.5 N 130-180E.
    If positve value, then the function returns -1 else +1.
    
    Input variables:
    lat,lon: 1-dim numpy arrays
    eof: 2-dim (lat,lon) numpy array with EOF (PDO) pattern
    Return value:
    integer number -1 or +1 (-1 if the EOF represents negative PDO phase)
    """

    is_lon=np.logical_and(lon>=130,lon<=180)
    is_lat=np.logical_and(lat>=32.5,lat<=42.5)
    buffer=eof[is_lat,:]
    res=buffer[:,is_lon]
    mean=np.nanmean(res)
    print(mean)
    return (-1*np.sign(mean)) # if SST anomaly negative then PDO index positive 

def save_result(mean,variance,lat,lon):
    """Saves the results from the ensemble average eof in netcdf file

    Input parameters:

    mean: field (2-dim array) with ensemble mean eof pattern
    variance: field (2-dim array) with ensemble variance of the eof members
    lat,lon: the sub-domain lat, lon coordinates
    copy_from_source: the field variable from the source  netcdf file
    
    The copy_from_source provides a netcdf source file (the input field
    data file to copy the information about dimensions, variables, units etc.
    """
    # ensemble mean
    xeofm=xarray.DataArray(mean,coords=[lat,lon],dims=['lat','lon'])
    xeofm.name='eofm'
    # 2018-07-19 corrected long_name and units attribute for eofs
    xeofm.attrs['long_name']="eigenvector ensemble mean"
    xeofm.attrs['units']='1' # eigenvectors of unit length
    xeofv=xarray.DataArray(variance,coords=[lat,lon],dims=['lat','lon'])
    # ensemble variance
    xeofv.name='eofv'
    xeofv.attrs['long_name']="eigenvector ensemble variance" 
    xeofv.attrs['units']='1' # eigenvectors of unit length 
    ds1=xarray.Dataset({'eofm':xeofm,'eofv':xeofv})
    print(ds1)
    outfile=MODEL+"_"+eofscen+"_"+v+"_"+eoftime+"_ensmean_ann_ano_resid_eof.nc"
    ds1.to_netcdf(OUTPATH+outfile,format="NETCDF4")
    print ("saved ensemble mean result in "+OUTPATH+outfile)
    return ds1


###############################################################################
# main
###############################################################################
v='SST' # file name variable
ncvar='eof' # variable in netcdf file
# Loop over scenarios                                                                                
iscen=0                                                                                                           
SCENCOLORLIST={"historical":"blue","rcp85":"red"}
STARTYRLIST={"historical":1996,"rcp85":2026}
ENDYRLIST={"historical":2005,"rcp85":2035}

for scen in ['historical']:     # only 'historical' in general                            
    nmodel=0
    eofscen=TRANSLATE[scen]['scen']      
    eoftime=TRANSLATE[scen]['time']      
    i=0
    for run in ENSEMBLELIST:
        nclat,nclon,eof=load_eof(scen,run,v,mode=MODE_PDO)
        if (i==0):
            nlat=len(nclat.data[:])
            nlon=len(nclon.data[:])
            nens=len(ENSEMBLELIST)
            ens_eof=np.zeros(shape=(nens,nlat,nlon))
            help_sign=np.zeros(nens) # sign convention for PDO index help array
            mean_eof=np.zeros(shape=(nlat,nlon))
        else:
            pass
        help_sign[i]=adjust_sign(nclat.data[:],nclon.data[:],eof)
        ens_eof[i,:,:]=eof*help_sign[i]
        if help_sign[i]<0:
            print(" ensemble # "+run)
            print("flip sign of EOF "+str(MODE_PDO)+" to match positive PDO phase pattern")
            print("invert eof pattern")
        mean_eof=np.nanmean(ens_eof,0)
        var_eof=np.nanvar(ens_eof,0) 
        i+=1
    iscen+=1

##############################################################################
# save results into netcdf file
##############################################################################
ds1=save_result(mean=mean_eof,variance=var_eof,lat=nclat,lon=nclon)
##############################################################################
# Begin a new figure
# Get the cartopy mapping object
fig = plt.figure(figsize=(12,9))
data_crs = ccrs.PlateCarree()
ax = plt.axes(projection=ccrs.Orthographic(central_longitude=180,\
    central_latitude=45.0,globe=None))
land = cfeature.NaturalEarthFeature(category='physical', name='land', scale='50m',
                                    facecolor=cfeature.COLORS['land'])
ocean = cfeature.NaturalEarthFeature(category='physical', name='ocean', scale='50m',
                                    facecolor='gray')

ax.add_feature(ocean,zorder=1)
ax.add_feature(land,zorder=2)
lon=nclon.data[:]
lat=nclat.data[:]
cont=ax.contour(lon, lat, mean_eof, 10,\
                colors="black",transform=data_crs,zorder=4)
contf=ax.pcolormesh(lon,lat, var_eof,\
                 cmap=get_cmap("jet"),transform=data_crs,zorder=3)

# Add a color bar
fig.colorbar(contf,ax=ax, shrink=.62)

# Set the map limits.  Not really necessary, but used for demonstration.
#ax.set_xlim( ) 
#ax.set_ylim()
# Add the gridlines
ax.gridlines(color="black", linestyle="dotted",zorder=5)
#ax.coastlines()
ax.set_xlabel("lon")
ax.set_ylabel("lat")
ax.set_title("Ensemble mean PDO pattern")

fig.show()

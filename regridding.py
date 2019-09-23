# Imports

#import matplotlib
import matplotlib.pyplot as plt
#matplotlib.use('TkAgg')
import numpy as np
import iris
import xarray as xr
import pandas as pd
import iris.plot as iplt
import cartopy as cr
import cartopy.img_transform as tr
import sys
import matplotlib.animation as ani
from matplotlib.animation import PillowWriter

# Load sea ice data into xarray
ds = xr.open_dataset('sea_ice_data/G10010_SIBT1850_v1.1.nc')
da = ds.seaice_conc
da = da.sel(time=slice('1979-01-01',None))

da.attrs['standard_name'] = None
dat = da.isel(time=0)
dat = dat.isel(latitude=slice(0,110),longitude=slice(0,465))
dat

## Convert into iris cube
#cube = dat.to_iris()
#cube.summary()

# Visualise the starting grid (plain)
#plt.figure()
#plt.title('SIC on a longitude-latitude grid')
#dat.plot.pcolormesh(cmap='Blues_r')
#ax = plt.gca()
##ax.coastlines(resolution='50m')
##ax.gridlines()
#plt.show()

# Visualise the starting grid (North Polar Stereo)
lats = dat.latitude.values
longs = dat.longitude.values
source_extent = (longs[0], longs[-1], lats[0], lats[-1])
#ax = plt.axes(projection=cr.crs.NorthPolarStereo())
ax = plt.axes(projection=cr.crs.AlbersEqualArea(central_latitude=60,central_longitude=60,standard_parallels=70))
#ax.set_extent([0,360,60,90],cr.crs.PlateCarree())
ax.set_extent([15,100,82,66],cr.crs.PlateCarree())
#dat.plot.pcolormesh('longitude','latitude',ax=ax,transform=cr.crs.PlateCarree(),cmap='Blues_r')
#dat.plot.imshow(transform=cr.crs.PlateCarree(),cmap='Blues_r')
#ax.pcolormesh(longs,lats,img,transform=cr.crs.PlateCarree(),cmap='Blues_r')
res = \
ax.imshow(dat,transform=cr.crs.PlateCarree(),cmap='Blues_r',extent=source_extent,\
origin='lower')
#print(type(ax))
#ax.coastlines()
#plt.show()
res = res.filled(fill_value=-10)
res = res[:,20:]
plt.figure()
plt.imshow(res,origin='lower',cmap='Blues_r')
plt.show()

# Automate image making
for i in range(da.time.values.shape[0]):
    dat = da.isel(latitude=slice(0,150),longitude=slice(0,500))
    dat = dat.isel(time=i)
    lats = dat.latitude.values
    longs = dat.longitude.values
    source_proj= cr.crs.PlateCarree()
    target_proj = cr.crs.NorthPolarStereo()
    source_extent = (longs[0], longs[-1], lats[0], lats[-1])
    target_extent = (-3402747.1802094635, 3396908.3796566334, -3331997.462588525,\
    3426439.3534922632)
    target_res = (754,750)
    
    res2, extent2 =\
    tr.warp_array(np.asanyarray(dat),source_proj=source_proj,source_extent=source_extent,\
    target_proj=target_proj,target_extent=target_extent, target_res=target_res,\
    mask_extrapolated=True)
    res2 = res2.filled(fill_value=-10)
    res2 = res2[100:370,380:650]
    np.save('ice_arrays/barentskara_{}'.format(i),res2)
    #plt.figure()
    #plt.imshow(res2,origin='lower',cmap='Blues_r')
    #plt.show()

plt.imshow(np.load('ice_arrays/barentskara_0.npy'),origin='lower',cmap='Blues_r')

# Animate

snapshots = [np.load('ice_arrays/barentskara_{}.npy'.format(i)) for i in range(420)]
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)
a = snapshots[0]
im = plt.imshow(a,interpolation='none',aspect='auto',origin='lower',cmap='Blues_r')

def animate_func(i):
    
    im.set_array(snapshots[i])
    return [im]

anim = ani.FuncAnimation(fig,animate_func,repeat=False)
anim.save('ice_arrays/gif_barentskara.gif',writer=PillowWriter(fps=5))
plt.show()

## Rotated pole sample cube
##rotated_psl = iris.load_cube('rotated_pole.nc')
#rot_ds = xr.open_dataset('rotated_pole.nc')
#rot_ds
#rot_dat = rot_ds.air_pressure_at_sea_level
#rot_dat
#rot_ds.rotated_latitude_longitude
#
## Visualise the target grid
#plt.figure()
#plt.title('Air temperature on a limited area rotated pole grid')
#rot_dat.plot.pcolormesh(cmap='Blues_r')
#ax = plt.gca()
##ax.coastlines(resolution='50m')
##ax.gridlines()
#plt.show()
#
#
## Regrid xarray.DataArray
#interp_dat = dat.interp_like(rot_dat)
#interp_dat
#dat
#
## Visualise the result 
#plt.figure()
#plt.title('SIC on a limited area rotated pole grid?')
#interp_dat.plot.pcolormesh(cmap='Blues_r')
#ax = plt.gca()
##ax.coastlines(resolution='50m')
##ax.gridlines()
#plt.show()
#
#x = np.linspace(0,1,10)
#y = np.linspace(1,2,20)
#xx,yy = np.meshgrid(x,y,indexing='ij')
#xx.shape
#yy.shape
#xx[-1,-2],yy[-1,-2]

# Regridding with cartopy 

source_proj = cr.crs.PlateCarree()
target_proj = cr.crs.NorthPolarStereo()
img = dat.values
img.shape
lats = dat.latitude.values
longs = dat.longitude.values
lats.shape
longs.shape
lats[0],lats[-1]
longs[0],longs[-1]
img.shape
source_extent = (longs[0], longs[-1], lats[0], lats[-1])
#target_extent = (-180,180,60,90)
target_res = (100,100)
warped_img = tr.warp_array(img, target_proj, source_proj=source_proj,\
source_extent=source_extent,target_res=target_res)
warped_img[0].shape
warped_img

plt.figure()
plt.imshow(warped_img[0])
plt.colorbar()
plt.show()

#dat
#plt.figure()
#ax = plt.axes(projection=cr.crs.NorthPolarStereo())
##ax.set_extent([180,-180,90,60],cr.crs.PlateCarree())
#plt.pcolormesh(dat, transform=cr.crs.PlateCarree())
#plt.colorbar()
#ax.coastlines()
#plt.show()

#  Visualise result
plt.figure()
plt.title('Air temperature on a limited area rotated pole grid')
ax = plt.axes(projection = cr.crs.PlateCarree())
plt.pcolormesh(warped_img[0],cmap='Blues_r')
#ax.coastlines(resolution='50m')
#ax.gridlines()
plt.colorbar()
plt.show()




mesh = tr.mesh_projection(proj,200,200)
mesh[0].shape
mesh[1].shape
mesh[2]

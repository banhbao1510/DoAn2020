import rasterio
# src = rasterio.open('/home/hoaixinhgai/Sentinel-download/out/tile_9000-4500.tif')
# Working dir
import os
print(os.getcwd())
src = rasterio.open('./out/tile_10370-10370.tif')
name = src.name
array = src.read(1)
shp = array.shape
print(shp)
print(name)
from matplotlib import pyplot
pyplot.imshow(array, cmap='pink')
pyplot.show()  
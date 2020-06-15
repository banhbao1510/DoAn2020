import numpy as np
import rasterio

# Read raster bands directly to Numpy arrays.
#
with rasterio.open('T47NPG_20200513T032539_TCI.jp2') as src:
    r, g, b = src.read()

# Combine arrays in place. Expecting that the sum will
# temporarily exceed the 8-bit integer range, initialize it as
# a 64-bit float (the numpy default) array. Adding other
# arrays to it in-place converts those arrays "up" and
# preserves the type of the total array.
total = np.zeros(r.shape)
for band in r, g, b:
    total += band
total /= 3

# Write the product as a raster band to a new 8-bit file. For
# the new file's profile, we start with the meta attributes of
# the source file, but then change the band count to 1, set the
# dtype to uint8, and specify LZW compression.
profile = src.profile
profile.update(dtype=rasterio.uint8, count=1, compress='lzw')

with rasterio.open('example-total.tif', 'w', **profile) as dst:
    dst.write(total.astype(rasterio.uint8), 1)
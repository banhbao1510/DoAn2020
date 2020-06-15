import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import os
dst_crs = 'EPSG:4326'
in_path = '/home/hoaixinhgai/Sentinel-download/'
input_filename = 'T47NPG_20200513T032539_TCI.jp2'

with rasterio.open(os.path.join(in_path, input_filename)) as src:
    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds)
    kwargs = src.meta.copy()
    kwargs.update({
        'crs': dst_crs,
        'transform': transform,
        'width': width,
        'height': height
    })

    with rasterio.open('/tmp/RGB.byte.wgs84.tif', 'w', **kwargs) as dst:
        for i in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, i),
                destination=rasterio.band(dst, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.nearest)
            dst.write(dst, indexes=i)
            # import matplotlib.pyplot as plt
            # plt.imshow()
        
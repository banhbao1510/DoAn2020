import os
from itertools import product
import rasterio as rio
from rasterio import windows

in_path = 'Z:/DataSets/planet_order_388369/20190806_092211_ss02_u0001/'
input_filename = '20190806_092211_ss02_u0001_visual.tif'

out_path = 'Z:/DataSets/planet_order_388369/20190806_092211_ss02_u0001/out/'
output_filename = 'tile_{}-{}.tif'

def get_tiles(ds, width=256, height=256):
    nols, nrows = ds.meta['width'], ds.meta['height']
    offsets = product(range(0, nols, width), range(0, nrows, height))
    big_window = windows.Window(col_off=0, row_off=0, width=nols, height=nrows)
    for col_off, row_off in  offsets:
        window =windows.Window(col_off=col_off, row_off=row_off, width=width, height=height).intersection(big_window)
        transform = windows.transform(window, ds.transform)
        yield window, transform


with rio.open(os.path.join(in_path, input_filename)) as inds:

    # tile_width, tile_height = int(inds.width/16),int(inds.height/16)
    tile_width, tile_height = 4500,4500

    meta = inds.meta.copy()

    for window, transform in get_tiles(inds,tile_width,tile_height):
        print(window)
        meta['transform'] = transform
        meta['width'], meta['height'] = window.width, window.height
        outpath = os.path.join(out_path,output_filename.format(int(window.col_off), int(window.row_off)))
        with rio.open(outpath, 'w', **meta) as outds:
            outds.write(inds.read(window=window))
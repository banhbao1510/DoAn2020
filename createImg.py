import os
from xml.dom import minidom
from itertools import product
import rasterio as rio
from rasterio import windows
from rasterio.transform import Affine
from rasterio.crs import CRS
import rasterio.warp
print(os.getcwd())
workingDir='/media/hoaixinhgai/GIAI TRI/Dataset'
out_path = '/home/hoaixinhgai/Sentinel-download/out/'
out_folder = ''
output_filename = 'tile_{}-{}.tif'
queryDir = os.path.join(workingDir,'query')
imageDir = os.path.join(workingDir,'imageDownload')
def get_info(folder):
    xs = []
    ys = []
    imgName=''
    for file in os.listdir(os.path.join(queryDir,folder)):
        if 'query_results' in file:
            x = float(file.split('_')[2])
            y = float(file.split('_')[3][:-4])
            xs.append(x)
            ys.append(y)
        if 'MTD' in file:
            mydoc = minidom.parse(os.path.join(queryDir,folder,file))
            items = mydoc.getElementsByTagName('IMAGE_FILE')
            # result = ''
            for item in items:
                if 'L1C' in item.childNodes[0].data:
                    if 'TCI' in item.childNodes[0].data:
                        imgName = item.childNodes[0].data.split('/')[-1]
                if 'L2A' in item.childNodes[0].data:
                    if 'TCI_10m' in item.childNodes[0].data:
                        imgName = item.childNodes[0].data.split('/')[-1]
        # out_folder = result
    if not os.path.isdir(os.path.join(workingDir,'Split',imgName)): 
        os.mkdir(os.path.join(workingDir,'Split',imgName))
    return imgName,xs,ys


    
def get_tiles(ds, width=256, height=256):
    nols, nrows = ds.meta['width'], ds.meta['height']
    offsets = product(range(0, nols, int(width/2)), range(0, nrows, int(height/2)))
    big_window = windows.Window(col_off=0, row_off=0, width=nols, height=nrows)
    for col_off, row_off in  offsets:
        window =windows.Window(col_off=col_off, row_off=row_off, width=width, height=height).intersection(big_window)
        if window.width == width and window.height == height:
            transform = windows.transform(window, ds.transform)
            yield window, transform

def selectInterestArea(imgName, x, y):
    out_folder = os.path.join(workingDir,'Split',imgName[:-4])
    with rio.open(os.path.join(imageDir, imgName)) as inds:

    # tile_width, tile_height = int(inds.width/16),int(inds.height/16)
        tile_width, tile_height = 1220,1220
        inv_transform = Affine.scale(1 / inds.transform.a, 1 / inds.transform.e) * Affine.translation(-inds.transform.xoff, -inds.transform.yoff)
        meta = inds.meta.copy()
        rasterio.warp.transform(crs0,inds.crs,[y],[x])
        a = rasterio.warp.transform(crs0,inds.crs,[y],[x])
        xPixel,yPixel=pixel_location = inv_transform*(a[0][0],a[1][0])
        print(pixel_location)      
        # print(count_sliding_window(inds.read(1)))
        for window, transform in get_tiles(inds,tile_width,tile_height):
            print(window)
            meta['transform'] = transform
            meta['width'], meta['height'] = window.width, window.height
            outpath = os.path.join(out_folder,output_filename.format(int(window.col_off), int(window.row_off)))
            if ((xPixel > window.col_off) & (xPixel < window.col_off + window.width) & (yPixel > window.row_off) & (yPixel < window.row_off + window.height)):
                with rio.open(outpath, 'w', **meta) as outds:
                    outds.write(inds.read(window=window))
            
crs0 = CRS.from_epsg(4326)
for folder in os.listdir(queryDir):
    print(folder)
    imgName,xs,ys = get_info(folder)
    for x,y in zip(xs,ys):
        selectInterestArea(imgName+'.jp2',x,y)

# selectInterestArea('T47PQQ_20200506T033529_TCI.jp2',12.679944,101.005028)


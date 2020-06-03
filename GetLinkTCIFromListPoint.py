from xml.dom import minidom
from datetime import datetime
import os,sys
import requests
import shutil
import csv

USER ='rerangst'
PASSWORD='56tyghbn'

url_search = "https://scihub.copernicus.eu/apihub/search?q="
os.system("rm *.xml ")
if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    value = "\\$value"
else:
    value = "$value"

def queryPoint (lat, lon):
    xml_query = 'query_results'+'_'+str(lat)+'_'+str(lon)
    MaxRecords = 100

    query_geom = 'footprint:"Intersects(%f,%f)"' % (lat, lon)
    query = '%s filename:%s*' % (query_geom, 'S2')

    link = r'{}{}&rows={}'.format(url_search, query, MaxRecords)
    resp = requests.get(link, auth=(USER, PASSWORD))

    with open(xml_query +'.xml', 'wb') as f:
        f.write(resp.content)
    resp.close()
    print("Query result in file: %s.xml "%xml_query)
    return(xml_query+'.xml')

def xml_parse(xml_file):
        mydoc = minidom.parse(xml_file)
        items = mydoc.getElementsByTagName('IMAGE_FILE')
        result = ''
        for item in items:
            if 'L1C' in item.childNodes[0].data:
                if 'TCI' in item.childNodes[0].data:
                    for text in item.childNodes[0].data.split('/'):
                        result = result + "Nodes('%s')/" % text
            if 'L2A' in item.childNodes[0].data:
                if 'TCI_10m' in item.childNodes[0].data:
                    for text in item.childNodes[0].data.split('/'):
                        result = result + "Nodes('%s')/" % text
                #print(result[:-3]+".jp2')/$value")
        return result[:-3]+".jp2')/$value"
def getLink(xmlPath):
    xml = minidom.parse(xmlPath)
    products = xml.getElementsByTagName("entry")
    newest = datetime.strptime("2015-06-13", '%Y-%m-%d')  # Sentinel-2 launch date
    min_cloud = 100
    downloadID = ''
    downloadLink = ''
    downloadFileName=''
    for prod in products:
        ident = prod.getElementsByTagName("id")[0].firstChild.data
        summary = prod.getElementsByTagName("summary")[0].firstChild.data
        for node in prod.getElementsByTagName("double"):
            (name, field) = list(node.attributes.items())[0]
            if field == "cloudcoverpercentage":
                cloud = float((node.toxml()).split('>')[1].split('<')[0])
                # print("cloud percentage = %5.2f %%" % cloud)
        date = summary.split(',')[0].replace('Date: ','').split('T')[0]
        datetime_obj = datetime.strptime(date, '%Y-%m-%d') 
        if  cloud< min_cloud:
            newest = datetime_obj
            min_cloud = cloud
            downloadID = ident
            
        # if datetime_obj > newest and cloud < min_cloud:
            # downloadFileName=filename
            # downloadLink = link
    # downloadID='ca6ed363-8fe8-43e7-90d0-c4ddd64ee28c'
    for prod in products:
        ident = prod.getElementsByTagName("id")[0].firstChild.data
        link = list(prod.getElementsByTagName("link")[0].attributes.items())[0][1]
        # to avoid wget to remove $ special character
        link = link.replace('$value', value)
        summary = prod.getElementsByTagName("summary")[0].firstChild.data
        filename=''
        for node in prod.getElementsByTagName("str"):
            (name, field) = list(node.attributes.items())[0]
            if field == "filename":
                filename = str(node.toxml()).split('>')[1].split('<')[0]
        if downloadID in ident:

            downloadFileName = filename
            downloadLink = link
            summary = prod.getElementsByTagName("summary")[0].firstChild.data
            date = summary.split(',')[0].replace('Date: ','').split('T')[0]
            
            for node in prod.getElementsByTagName("double"):
                (name, field) = list(node.attributes.items())[0]
                if field == "cloudcoverpercentage":
                    cloud = float((node.toxml()).split('>')[1].split('<')[0])
            print("+)Select product with:")
            print("\t-)ID: ",downloadID)
            print("\t-)Date: ",date)
            print("\t-)cloud percentage = %5.2f %%" % cloud)

    if cloud > 10:
      print('Cannot find satisfied image !')
      return
    if not os.path.exists(downloadID):
        os.mkdir(downloadID)
    # else:    
    #     print("Directory " , downloadID ,  " already exists")

    xmlname = 'MTD_' + downloadFileName.split("_")[1]
    downloadLink = downloadLink.replace("\\$value","")
    linkxml = downloadLink + "Nodes('%s')" % downloadFileName + "/Nodes('%s.xml')" % xmlname + "/$value"
    resp = requests.get(linkxml, auth=(USER, PASSWORD))

    with open(downloadID+ "/"+ xmlname +'.xml', 'wb') as f:
        f.write(resp.content)
    resp.close()
    

    xmlresult = xml_parse(downloadID+ "/"+ xmlname +'.xml')
    linktci = downloadLink + "Nodes('%s')" % downloadFileName + "/" + xmlresult
    with open(downloadID + "/" + 'link.txt','w') as f:
        f.write(linktci)
    
    shutil.copyfile(xmlPath,downloadID+"/"+xmlPath.split('/')[-1])
# os.chdir('../')
with open('/content/AsiaAirports.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    data = list(csv_reader)
    row_count = len(data)

continueIdx=410
out_dir="/content/out"
if os.path.exists(out_dir):
    if continueIdx==0:
        os.system("rm -r %s"%out_dir)
else:
    os.mkdir(out_dir)
os.chdir(out_dir)
for i,row in enumerate(data):
    if i>=continueIdx:
        print("------------------------Point:(%s/%s)---------------------------"%(i,row_count))
        xmlPath = queryPoint(float(row[4]),float(row[5]))
        getLink(xmlPath)
#queryPoint(1.41695,103.867653)
#getLink('/home/hoaixinhgai/Sentinel-download/query_results_1.41695_103.867653.xml')
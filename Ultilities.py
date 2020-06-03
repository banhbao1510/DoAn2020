import os
import sys
import math
import optparse
from xml.dom import minidom

def xml_parse(xml_file):
    mydoc = minidom.parse(xml_file)
    items = mydoc.getElementsByTagName('IMAGE_FILE')
    for item in items:
        if 'TCI' in item.childNodes[0].data:
            result = ''
            for text in item.childNodes[0].data.split('/'):
                result = result + "Nodes('%s')/" % text
            #print(result[:-3]+".jp2')/$value")
    return result[:-3]+".jp2')/$value"
# print(xml_parse('MTD_MSIL1C.xml'))
def Merge_LinkDownload(dir):
    #dir ='/home/hoaixinhgai/Downloads/file410/content/out'
    listLink=''
    count = 0
    for folder in os.listdir(dir):
        with open(os.path.join(dir,folder,'link.txt'),'r') as f:
            a = f.readline()
            count = count + 1
            listLink=listLink+a+'\n'
            # print(a)
    with open('listLink.txt','w') as f:
        f.write(listLink)
    print(count)

def Count_SatisfiedImg(dir):
    #dir = '/home/hoaixinhgai/Dataset/out'
    listMTD = ''
    count = 0
    for folder in os.listdir(dir):
        for file in os.listdir(os.path.join(dir,folder)):
            if 'MTD' in file:
                path = os.path.join(dir,folder,file)
                mydoc = minidom.parse(path)
                item = mydoc.getElementsByTagName('Cloud_Coverage_Assessment')[0]
                cloud_percentage = float(item.childNodes[0].data)
                if cloud_percentage < 10:
                    count = count + 1
    print(count)

import csv
import requests

import numpy as np
# import urllib.request as urllib2

from math import radians, cos, sin, asin, sqrt

def GetDistance(A, B):
    ra = 6378140
    rb = 6356755
    flatten = 0.003353 

    # change angle to radians
    radLatA = np.radians(A[:,0])
    radLonA = np.radians(A[:,1])
    radLatB = np.radians(B[:,0])
    radLonB = np.radians(B[:,1])

    pA = np.arctan(rb / ra * np.tan(radLatA))
    pB = np.arctan(rb / ra * np.tan(radLatB))
    
    x = np.arccos( np.multiply(np.sin(pA),np.sin(pB)) + np.multiply(np.multiply(np.cos(pA),np.cos(pB)),np.cos(radLonA - radLonB)))
    c1 = np.multiply((np.sin(x) - x) , np.power((np.sin(pA) + np.sin(pB)),2)) / np.power(np.cos(x / 2),2)
    c2 = np.multiply((np.sin(x) + x) , np.power((np.sin(pA) - np.sin(pB)),2)) / np.power(np.sin(x / 2),2)
    dr = flatten / 8 * (c1 - c2)
    distance = 0.001 * ra * (x + dr)

    return distance

def DownloadMask():
    url = 'http://data.nhi.gov.tw/Datasets/Download.ashx?rid=A21030000I-D50001-001&l=https://data.nhi.gov.tw/resource/mask/maskdata.csv'
    FileData = requests.get(url).text.split("\n", 1)[1]
    
    with open('data/mask.csv', 'w') as fp:
        fp.write(FileData)

def LoadMask():
    data = {}
    odata = csv.reader(open('data/mask.csv', 'r'))
    
    for dt in odata:
        data[dt[0]] = [dt[1], dt[4], dt[5]]
    
    return data

def LoadDis():
    DisAll = []
    data = [x for x in csv.reader(open('data/points.csv', 'r'))]
    [DisAll.append([float(x[7]), float(x[6])]) for x in data]
    return DisAll
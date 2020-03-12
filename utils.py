import csv
import requests

import numpy as np
# import urllib.request as urllib2

from datetime import datetime
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

def LoadData():
    dist_data = {}
    ret_data = []
    nuse_data = []

    for x in csv.reader(open('data/points.csv', 'r')):
        dist_data[x[0]] = [x[7], x[6]]

    for data in csv.reader(open('data/mask.csv', 'r')):
        if data[0] in dist_data:
            data.extend(dist_data[data[0]]), ret_data.append(data)
    
    return ret_data

def CalcTime(old):
    now = datetime.now().strftime('%Y %m %d %H %M %S')
    interval = datetime.strptime(now, '%Y %m %d %H %M %S') - datetime.strptime(old, '%Y/%m/%d %H:%M:%S')
    return (interval.days, interval.seconds)
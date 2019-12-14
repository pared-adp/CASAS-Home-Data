# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 14:18:30 2019

@author: adpaw
"""

#from prefixspan import PrefixSpan
from prefixspan import PrefixSpan
import pandas as pd
import numpy as np

outfile = open('results.txt', 'w')

data = pd.read_csv('updated.csv', names=["Date Time", "Sensor", "Message", "Activity"])
data['Activity'].replace(np.nan, 'Standby', inplace = True)
dataList= data.values.tolist()
#replace nan with Standby

#print(data.Activity.unique())
ps = PrefixSpan(dataList)

coverage = [[] for i in range(len(dataList))]
def cover(patt, matches):
    for i, _ in matches:
        coverage[i] = max(coverage[i], patt, key=len)
        
test = ps.frequent(10, callback=cover)
#print(coverage)

for line in coverage:
    outfile.write(str(line) + '\n')
    

outfile.close()

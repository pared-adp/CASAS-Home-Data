# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 20:35:05 2019

@author: adpaw
"""

#preproccessing for features
import pandas as pd
import numpy as np
import csv
from datetime import datetime

maxLength = 0
temp = 0
test = open("update.csv", "w")
with open('month.txt', 'r') as f:
    file_reader = csv.reader(f, delimiter='\t')
    newLine = ''
    for line in file_reader:
        newLine = ",".join(str(bit) for bit in line) # add commas between words
        test.write(newLine + '\n')
                      
test.close()
            
##DATA CLEANING##       
data = pd.read_csv('updated.csv', names=["Date Time", "Sensor", "Message", "Activity", "Status"])
data['Activity'].replace(np.nan, 'Standby', inplace=True)
data['Status'].replace(np.nan, 'Waiting', inplace=True)

win_indx = 0
start = 0
sensorNames = data.Sensor.unique()
feature = pd.DataFrame(columns = sensorNames)
window = 100
date_str = '%Y-%m-%d %H:%M:%S.%f'
#print(feature.head())
diff = []
last_event = []
for row in range(0,len(data)):
    if (row  + 1) % window == 0:
        test = data.iloc[win_indx:row]
        p1= test['Sensor'].value_counts() #sensor count features
        feature = feature.append(p1, ignore_index = True)
        
        #time1 = str(test['Date Time'].iat[0]) #converts to datetime structures to find difference
        #time2 = str(test['Date Time'].iat[-1])
        d1 = datetime.strptime(str(test['Date Time'].iat[0]), date_str)
        d2 = datetime.strptime(str(test['Date Time'].iat[-1]), date_str)
        diff.append(int((d2-d1) .total_seconds() / 60))
        last_event.append(test.Activity.unique()[-1])
        win_indx += window
#generating additional feature values
feature['Time Difference'] = np.array(diff)
feature['Window Length'] = len(test)
feature['Label'] = np.array(last_event)
feature.replace(np.nan, 0, inplace = True)
feature['Label'] = feature['Label'].astype('category')
feature['Label_cat'] = feature['Label'].cat.codes
feature.to_csv('feature.csv') 

#encoding categorical labels

#print(feature.head(5))#window length feature       
  

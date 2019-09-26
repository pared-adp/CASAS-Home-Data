# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 14:18:38 2019

@author: Angelina Paredes
"""

import pandas as pd
import numpy as np
import csv

data = pd.read_csv('data.txt', sep = '\t', header = None) # parses data into dataframe
del data[4] #deletes last column all nan
data.columns = ['Date Time','Sensor Name','Message','Type']
print(data.Type.unique()) #different senors in the testbed


    




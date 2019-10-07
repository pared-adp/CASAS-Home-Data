"""
cb: Bryton LeValley
demonstration of separating rooms for home project
might be an easier way, but I made the output files easily readable by postgres
"""


#pip install pathlib in terminal this is for mac compatability Just in case
from pathlib import Path
import csv
from datetime import datetime as time

# !!!!change this if file is located somewhere else
start = time.now()
data_path = "data/new_data.txt"
data_length = 3
i = 0


#initialize files
sensor_302 = open('sensor_302.csv', 'w')
sensor_304 = open('sensor_304.csv', 'w')
sensor_401 = open('sensor_401.csv', 'w')
sensor_402 = open('sensor_402.csv', 'w')
sensor_319 = open('sensor_319.csv', 'w')
sensor_306 = open('sensor_306.csv', 'w')
sensor_318 = open('sensor_318.csv', 'w')
sensor_320 = open('sensor_320.csv', 'w')
sensor_321 = open('sensor_321.csv', 'w')
sensor_322 = open('sensor_322.csv', 'w')
sensor_308 = open('sensor_308.csv', 'w')
sensor_307 = open('sensor_307.csv', 'w')
sensor_323 = open('sensor_323.csv', 'w')
sensor_310 = open('sensor_310.csv', 'w')
sensor_309 = open('sensor_309.csv', 'w')
sensor_301 = open('sensor_301.csv', 'w')
sensor_302 = open('sensor_302.csv', 'w')
sensor_303 = open('sensor_303.csv', 'w')
sensor_311 = open('sensor_311.csv', 'w')
sensor_314 = open('sensor_314.csv', 'w')
sensor_305 = open('sensor_305.csv', 'w')
sensor_317 = open('sensor_317.csv', 'w')
sensor_316 = open('sensor_316.csv', 'w')
sensor_312 = open('sensor_312.csv', 'w')
sensor_313 = open('sensor_313.csv', 'w')
sensor_315 = open('sensor_315.csv', 'w')
lost_sensors = open('lost_sensor.csv', 'w')


#used for counting missing sensors
j = 0
error = 0

# reads the original data
with open(Path(data_path), 'r') as infile:
    file_reader = csv.reader(infile, delimiter='\t')

    for row in file_reader:
        row_string = ''
        i = i + 1

        # steps through each line in original file
        for x in range(len(row)):

            # checks if not Null and adds each row to a new row string while replacing the tab separator with commas
            if row[x] != '':
                row_string += row[x]
                row_string += ','

        # add an extra comma if there is no notes in the row
        # this makes the files work better with the pandas functions

        if len(row) <= data_length:
            for x in range(len(row),data_length):
                row_string += ','

        #deletes the last comma if the data has any extra information
        else:
            row_string = row_string[:-1]

        # try catches errors in the orginal dataset
        try:
            # puts the row into specific room
            #for the person not familiar with python elif is simply else if
            if '302' in row[1]:
                sensor_302.write('\n'+row_string)
            elif '304' in row[1]:
                sensor_304.write('\n'+row_string)
            elif '401' in row[1]:
                sensor_401.write('\n'+row_string)
            elif '402' in row[1]:
                sensor_402.write('\n'+row_string)
            elif '319' in row[1]:
                sensor_319.write('\n'+row_string)
            elif '306' in row[1]:
                sensor_306.write('\n'+row_string)
            elif '318' in row[1]:
                sensor_318.write('\n'+row_string)
            elif '320' in row[1]:
                sensor_320.write('\n'+row_string)
            elif '321' in row[1]:
                sensor_321.write('\n'+row_string)
            elif '322' in row[1]:
                sensor_322.write('\n'+row_string)
            elif '308' in row[1]:
                sensor_308.write('\n'+row_string)
            elif '307' in row[1]:
                sensor_307.write('\n'+row_string)
            elif '323' in row[1]:
                sensor_323.write('\n'+row_string)
            elif '310' in row[1]:
                sensor_310.write('\n'+row_string)
            elif '309' in row[1]:
                sensor_309.write('\n'+row_string)
            elif '301' in row[1]:
                sensor_301.write('\n'+row_string)
            elif '303' in row[1]:
                sensor_303.write('\n'+row_string)
            elif '311' in row[1]:
                sensor_311.write('\n'+row_string)
            elif '314' in row[1]:
                sensor_314.write('\n'+row_string)
            elif '305' in row[1]:
                sensor_305.write('\n'+row_string)
            elif '317' in row[1]:
                sensor_317.write('\n'+row_string)
            elif '316' in row[1]:
                sensor_316.write('\n'+row_string)
            elif '312' in row[1]:
                sensor_312.write('\n'+row_string)
            elif '313' in row[1]:
                sensor_313.write('\n'+row_string)
            elif '315' in row[1]:
                sensor_315.write('\n'+row_string)
            else:
                lost_sensors.write('\n'+row_string)
        #when row[1] does not exist do this
        except IndexError:
            error += 1
            print(f'index error at {i}')

        #print out each run by 100000

        #this is simply for metrics
        if i%10000 == 0:
            print(time.now()-start)
            print(i)

"""
notes about the output file:
the comma at the end means there is another item at the end. it is just a empty string
"""
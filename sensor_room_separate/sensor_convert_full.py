"""
cb: Bryton LeValley
demonstration of separating rooms for home project
might be an easier way, but I made the output files easily readable by postgres
"""


#pip install pathlib in terminal this is for mac compatability Just in case
from pathlib import Path
import csv
import datetime as datetime

# !!!!change this if file is located somewhere else
start = datetime.now()
data_path = "data/data.txt"
data_length = 3
i = 0

# this is the list for room sensors
Bedroom_red = ('M047', 'M045', 'M046', 'M048','M049', 'M050', 'M044', 'M043','D004', 'L001', 'T004')
bedroom_blue = ('E002', 'T005', 'M042', 'L002')
bedroom_purple = ('D003', 'M030', 'M036', 'M035', 'M034', 'M031', 'T003', 'M032', 'M033', 'L004')
hallway_orange = ('M027','L003','M028','M029')
bathroom_brown = ('M037','D005','M038','M039','L006', 'M040', 'D006', 'M041','L007','L005','F001', 'F002', 'P001')
livingroom_maroon = ('M004', 'M003', 'R002','M002', 'D013','I011', 'I012', 'M005', 'M006', 'T001', 'M007', 'M001',
                     'M011', 'E001', 'M010', 'I008', 'I009', 'M009', 'M008','D002', 'M012', 'M013', 'M014', 'M015',
                     'L008')
hallway_pink = ('M026', 'M025', 'L009', 'M024', 'D001', 'D012', 'M019', 'M020', 'L011', 'M023', 'M022', 'M021')
kitchen_yellow = ('D008', 'D009', 'D010', 'R001', 'M016', 'L010', 'M017', 'T002', 'M018', 'M051', 'D011', 'D016',
                  'D017', 'I007', 'D014', 'D015', 'I006', 'I010', 'I001', 'I002', 'I003', 'I004', 'I005', 'A001',
                  'A002', 'A003', 'D007')

#initialize strings
bedroom_red_out = ''
bedroom_purple_out = ''
hallway_orange_out = ''
bedroom_blue_out = ''
bathroom_brown_out = ''
livingroom_maroon_out = ''
hallway_pink_out = ''
kitchen_yellow_out = ''

lost_sensors = ''
lost_sensor_list = []

#used for counting missing sensors
j = 0
error = 0

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


        try:
            # puts the row into specific room
            if row[1] in Bedroom_red:
                bedroom_red_out = bedroom_red_out + '\n' + row_string
            elif row[1] in bedroom_purple:
                bedroom_purple_out = bedroom_purple_out + '\n' + row_string
            elif row[1] in bathroom_brown:
                bathroom_brown_out = bathroom_brown_out + '\n' + row_string
            elif row[1] in livingroom_maroon:
                livingroom_maroon_out = livingroom_maroon_out + '\n' + row_string
            elif row[1] in hallway_pink:
                hallway_pink_out = hallway_pink_out + '\n' + row_string
            elif row[1] in hallway_orange:
                hallway_orange_out = hallway_orange_out + '\n' + row_string
            elif row[1] in kitchen_yellow:
                kitchen_yellow_out = kitchen_yellow_out + '\n' + row_string
            elif row[1] in bedroom_blue:
                bedroom_blue_out = bedroom_blue_out + '\n' + row_string
            else:
                lost_sensors = lost_sensors + '\n' + row_string

                #test for extra sensors not accounted for
                j += 1
                if row[1] not in lost_sensor_list:
                    lost_sensor_list.append(row[1])
        except IndexError:
            error += 1
            print(f'index error at {i}')

        #print out each run by 100000
        if i%10000 == 0:
            print(datetime.now()-start)
            print(i)
        # breaks at 100000 rows for demo purposes
        #if i > 100000:
            #break

#shows the amount of roomless sensors
print(f"lost sensors: {lost_sensor_list}")
print(f"{j} lost sensors")

#writes csv files for each location
with open('bedroom_red.csv', 'w+') as file:
    file.write(bedroom_red_out)

with open('bedroom_blue.csv', 'w+') as file:
    file.write(bedroom_blue_out)

with open('bedroom_purple.csv', 'w+') as file:
    file.write(bedroom_purple_out)

with open('bathroom_brown.csv', 'w+') as file:
    file.write(bathroom_brown_out)

with open('livingroom_maroon.csv', 'w+') as file:
    file.write(livingroom_maroon_out)

with open('hallway_orange.csv', 'w+') as file:
    file.write(hallway_orange_out)

with open('hallway_pink.csv', 'w+') as file:
    file.write(bedroom_blue_out)

with open('kitchen_yellow.csv', 'w+') as file:
    file.write(bedroom_blue_out)

with open('lost_sensors.csv', 'w+') as file:
    file.write(lost_sensors)

"""
notes about the output file:
the comma at the end means there is another item at the end. it is just a empty string
"""
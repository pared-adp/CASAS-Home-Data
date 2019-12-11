"""
activity regonition
"""
import inline as inline
import matplotlib
from matplotlib import pyplot as plt
# %matplotlib inline #should be working but isnt...
from pathlib import Path
import csv
from datetime import datetime as time
import numpy as np
# import separate_rooms_usethis # for whatever reason, this file cant be found

start = time.now()
data_path = "data/data.txt"
data_length = 3
i = 0

# Room Sensor List
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

# Initialized Strings
bedroom_red_out = open('bedroom_red.csv','w')
bedroom_purple_out = open('bedroom_purple.csv','w')
hallway_orange_out = open('hallway_orange.csv','w')
bedroom_blue_out = open('bed_room_blue','w')
bathroom_brown_out = open('bathroom_brown','w')
livingroom_maroon_out = open('livingroom_maroon.csv','w')
hallway_pink_out = open('hallway_pink.csv','w')
kitchen_yellow_out = open('kitchen_yellow.csv','w')

lost_sensors = ''
lost_sensor_list = []

# Use for counting missing sensors
j = 0
error = 0

LABELS = [
    'Bedroom',
    'BatteryPercentage',
    'BatteryVolt',
    'MotionSensor',
    'R1_Sensor',
    'R2_Sensor'
]

LABEL = 'ActivityEncoded'

# Plots activity for each separated activity
def plot_activity(activity, data):
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3,
         figuresize=(15, 10),
         sharex=True)
    plot_axis(ax0, data['timestamp'], data['x-axis'], 'X-Axis')
    plot_axis(ax1, data['timestamp'], data['y-axis'], 'Y-Axis')
    plot_axis(ax2, data['timestamp'], data['z-axis'], 'Z-Axis')
    plt.subplots_adjust(hspace = 0.2)
    fig.suptitle(activity)
    plt.subplots_adjust(top = 0.90)
    plt.show()

# this will plot the data on different axis
def plot_axis(ax, x, y, title):
    ax.plot(x,y,'r')
    ax.set_title(title)
    ax.x_axis.set_visbile(False)
    ax.set_ylimit([min(y) - np.std(y), max(y) + np.std(y)])
    ax.set_xlimit([min(x), max(x)])
    ax.grid(True)


# Close files
bedroom_blue_out.close()
bedroom_purple_out.close()
bathroom_brown_out.close()
hallway_pink_out.close()
hallway_orange_out.close()
kitchen_yellow_out.close()
livingroom_maroon_out.close()
bedroom_red_out.close()

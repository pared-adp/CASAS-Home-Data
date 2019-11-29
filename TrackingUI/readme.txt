Sensor statistics:
Set the start time and current time. When refreshed the tables will output curent status of the sensors 
the average duration of sensors (between the start and current datetime) and the last activation time according 
to the current datetime.
WARNING: queries for motion and light sensors will take a couple minutes if the difference between current 
and start is over a few weeks.

sensor health check:
 type in desired sensor in box from door, fan, item, motion, and lightswitch databases. a histogram will output 
 with data for that sensor from the start datetime to the current datetime when refreshed.
 WARNING: if inputing a new sensor the histgram window(x, and y range) will remain the same as the first sensor 
 input, you will have to change the ranges manually.
 
 Battery Trascking:
 according to the current datetime hitting refresh will output the current charge, the drainrate in percent/day
 and the days to the batterys dropping below 50% (which is when I think batterys should be replaced but this can
 be changed easily). Refreshing also creates a monthly change list where if the battery will drop below 50% in
 the next month it will be reccomended for changing.
 note: the start datetime does nothing for this tab.


notes:
This code requires postgres, and pgadmin on your computer
the designer application can be accessed by typing 'designer' into your development environment's terminal


repositories:
pip install PyQt5
pip install psycopg2
pip install pyqt5-tools # to access the designer APP
pip install pyqtgraph
pip install datetime
pip install python-dateutil

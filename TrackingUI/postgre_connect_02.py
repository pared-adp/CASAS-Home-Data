import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QListWidgetItem
from PyQt5 import uic

import numpy as np
import psycopg2

from dateutil import parser
from datetime import timedelta

import pyqtgraph as pg

qtCreatorFile = "datetime_list_01.ui" # Enter designer file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class outputGUI(QMainWindow):

    def __init__(self):
        super(outputGUI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #all butuons/user inputs should be initialized here
        self.ui.pushButton_refresh_door.clicked.connect(self.display_door)
        self.ui.pushButton_refresh_fan.clicked.connect(self.display_fan)
        self.ui.pushButton_refresh_item.clicked.connect(self.display_item)
        self.ui.pushButton_refresh_motion.clicked.connect(self.display_motion)
        self.ui.pushButton_refresh_light.clicked.connect(self.display_light)
        self.ui.pushButton_refresh_temp.clicked.connect(self.display_temp)
        self.ui.pushButton_refresh_batt.clicked.connect(self.display_batt)
        self.ui.pushButton_refresh_lightswitch.clicked.connect(self.display_lightswitch)
        self.ui.pushButton_hist.clicked.connect(self.display_histogram)

    def executeQuery(self,sql_str):
        """executes an sql query"""
        try:
            conn = psycopg2.connect("dbname='smarthome' user='postgres' host='smarthome.csjinfsewgpk.us-east-2.rds.amazonaws.com' password='12345678'")
        except:
            print('Unable to connect to database')
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()
        result = cur.fetchall()
        conn.close()
        return result

    def convert(self, QDateTime):
        """converts the datetime object read in from QTdesigner into SQL format"""
        return"'" + QDateTime.toString("yyyy-MM-dd HH:mm:ss") + "'"

    def display_battery_status(self, db_name, table_object, list_object):
        """displays battery health"""

        # get the user selected time
        now_time = self.ui.dateTimeEdit_start.dateTime()
        date_string = self.convert(now_time)
        print(date_string)

        # finds all distinct items in the database
        sql_str = f"SELECT DISTINCT(name) FROM {db_name} ORDER BY name;"
        item_list = self.executeQuery(sql_str)
        print(item_list)
        list_length = len(item_list)

        # set the table dimensions for the output table
        table_object.setColumnCount(4)
        table_object.setRowCount(list_length)
        table_object.setHorizontalHeaderItem(0,QTableWidgetItem("Item"))
        table_object.setHorizontalHeaderItem(1, QTableWidgetItem("CurStatus"))
        table_object.setHorizontalHeaderItem(2, QTableWidgetItem("drainRate"))
        table_object.setHorizontalHeaderItem(3, QTableWidgetItem("daysToLow"))

        sql_str = f"SELECT sdatetime, name, message, drainRate FROM {db_name} bp, battDrainRate bdr " \
            f"WHERE bp.name = bdr.battID AND sdatetime <= {date_string};"

        print(sql_str)
        query_result = self.executeQuery(sql_str)
        query_length = len(query_result)

        print(query_result)
        i = 0
        warning_list = []
        # this for loop finds every unique sensor in the DB and outputs its smessage to the table
        for item in item_list:
            print(item[0])
            a = query_length
            # this loop looks backwards from the last datapoint with the currently selected datetime and
            # finds the last output of each item
            while a > 0:
                # this is before the rest of the code because matrices in python count from 0; so max row is length - 1
                a = a - 1
                if item[0] == query_result[a][1]:
                    print(a)
                    now_batt_perc = float(query_result[a][2])
                    batt_drain_rate = query_result[a][3]
                    if batt_drain_rate is not None and batt_drain_rate > 0:
                        day_output = round((now_batt_perc-50)/batt_drain_rate)
                        if day_output < 30:
                            warning_list.append(item[0])
                        if day_output < 0:
                            day_output = "CHANGENOW"

                    else:
                        day_output = "GOOD"

                    table_object.setItem(i, 0, QTableWidgetItem(item[0]))
                    table_object.setItem(i, 1, QTableWidgetItem(query_result[a][2]))
                    table_object.setItem(i, 2, QTableWidgetItem(str(query_result[a][3])))
                    table_object.setItem(i, 3, QTableWidgetItem(str(day_output)))
                    break
            else:
                table_object.setItem(i, 0, QTableWidgetItem(item[0]))
                table_object.setItem(i, 1, QTableWidgetItem("NODATA"))
                table_object.setItem(i, 2, QTableWidgetItem("NODATA"))
                table_object.setItem(i, 3, QTableWidgetItem("NODATA"))

            i = i+1


        for item in warning_list:
            list_object.addItem(QListWidgetItem(item))

    def display_histogram(self):
        """displays a histogram to check the health of a sensor"""
        # get the user selected time
        start_time = self.ui.dateTimeEdit_start.dateTime()
        now_time = self.ui.dateTimeEdit_end.dateTime()
        date_string_start = self.convert(now_time)
        date_string_end = self.convert(start_time)
        print("from ", date_string_start, " to ", date_string_end)

        #finds all sensors that a histogram can be made out of
        sql_str = "SELECT DISTINCT(sname), 'Door' FROM Door UNION SELECT DISTINCT(sname), 'Fan' FROM fan UNION " \
                  "SELECT DISTINCT(sname), 'L' FROM L UNION SELECT DISTINCT(sname), 'Item' FROM item UNION " \
                  "SELECT DISTINCT(sname), 'Motion' FROM Motion ORDER BY sname;"
        print(sql_str)
        query_result = self.executeQuery(sql_str)
        sensor_list = [row[0] for row in query_result]
        print(sensor_list)
        sensor_choice = self.ui.lineEdit_hist.text()
        print(sensor_choice)
        if sensor_choice in sensor_list:
            print("choice in list")
            for item in query_result:
                if item[0] == sensor_choice:
                    loc = item[1]
                    break
            sql_str = f"SELECT sdatetime, sname, smessage FROM {loc} WHERE sdatetime <= {date_string_end} AND" \
                f" sdatetime >= {date_string_start} AND sname = '{sensor_choice}';"
            print(sql_str)
            query_result = self.executeQuery(sql_str)
            print(query_result)

            a = len(query_result)
            on_bool = ["PRESENT", "ON", "OPEN"]
            off_bool = ["ABSENT", "OFF", "CLOSE"]
            output = []
            on = None
            off = None

            while a > 0:
                a = a - 1
                if query_result[a][2] in off_bool:
                    off = parser.parse(query_result[a][0])
                    # print(off)
                elif query_result[a][2] in on_bool:
                    on = parser.parse(query_result[a][0])
                    # print("on", on)
                    if off is not None:
                        # print("test", off-on)
                        output.append((off-on).total_seconds())
                        on = None
                        off = None
            print(output)

            y, x = np.histogram(output, bins=20)

            ## notice that len(x) == len(y)+1
            ## We are required to use stepMode=True so that PlotCurveItem will interpret this data correctly.
            curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 200, 100))
            self.ui.graphWidget.clear()
            self.ui.graphWidget.setTitle(sensor_choice)
            self.ui.graphWidget.setLabel('bottom', 'Seconds', color='red', size=20)
            self.ui.graphWidget.addItem(curve)

        else:
            print("ERROR choice not in list")

    def display_binary_status(self, db_name, table_object, string_bool):
        """displays status of all items in list"""

        # get the user selected time
        start_time = self.ui.dateTimeEdit_start.dateTime()
        now_time = self.ui.dateTimeEdit_end.dateTime()
        date_string_start = self.convert(now_time)
        date_string_end = self.convert(start_time)
        print("from ", date_string_start, " to ", date_string_end)

        # finds all distinct items in the database
        sql_str = f"SELECT DISTINCT(sname) FROM {db_name} ORDER BY sname;"
        item_list = self.executeQuery(sql_str)
        print(item_list)
        list_length = len(item_list)

        # set the table dimensions for the output table
        table_object.setColumnCount(4)
        table_object.setRowCount(list_length)
        table_object.setHorizontalHeaderItem(0,QTableWidgetItem("Item"))
        table_object.setHorizontalHeaderItem(1, QTableWidgetItem("Cur_Status"))
        table_object.setHorizontalHeaderItem(2, QTableWidgetItem("Avg_on_duration"))
        table_object.setHorizontalHeaderItem(3, QTableWidgetItem("last_on_duration"))

        sql_str = f"SELECT sdatetime, sname, smessage FROM {db_name} WHERE sdatetime <= {date_string_end} AND" \
            f" sdatetime >= {date_string_start};"
        # note for the sql_str it might be good to get only a months worth of data
        print(sql_str)
        query_result = self.executeQuery(sql_str)
        query_length = len(query_result)

        print(query_result)
        i = 0
        # this for loop finds every unique sensor in the DB and outputs its smessage to the table
        for item in item_list:
            print(item[0])
            a = query_length
            last_status = "NODATA"
            last_on = None
            last_off = None
            on_duration = timedelta(0)
            num_for_avg = 0
            on = None
            off = None
            # this loop looks backwards from the last datapoint with the currently selected datetime and
            # finds the last output of each item
            while a > 0:
                # this is before the rest of the code because matrices in python count from 0; so max row is length - 1
                a = a - 1
                if item[0] == query_result[a][1]:
                    #print(query_result[a][2])
                    #print(string_bool[0])
                    if query_result[a][2] == string_bool[0]:
                        off = parser.parse(query_result[a][0])
                        #print(off)
                    elif query_result[a][2] == string_bool[1]:
                        on = parser.parse(query_result[a][0])
                        #print("on", on)
                        if off is not None:
                            #print("test", off-on)
                            on_duration = on_duration + (off-on)
                            num_for_avg = num_for_avg + 1
                            on = None
                            off = None

                    if last_on is None:
                        if query_result[a][2] == string_bool[1]:
                            last_on = parser.parse(query_result[a][0])
                            if last_off is None:
                                last_status = query_result[a][2]
                                print(now_time)
                                last_off = parser.parse(date_string_end)
                        elif query_result[a][2] == string_bool[0]:
                            last_status = query_result[a][2]
                            last_off = parser.parse(query_result[a][0])
                        else:
                            last_on = "NODATA"
                            last_off = "NODATA"
                            print("break")
                            break

            print(f"for item {item[0]}")
            print(on_duration, num_for_avg)
            print(last_off,last_on)
            if last_on == "NODATA":
                last_duration_on = "NODATA"
                print(last_duration_on)
            elif last_on is not None and last_off is not None:
                last_duration_on = str(last_off-last_on)[:-4]
            else:
                last_duration_on = "NODATA"

            if num_for_avg > 0:
                avg_duration_on = str(on_duration/num_for_avg)[:-4]
            else:
                avg_duration_on = "NODATA"

            table_object.setItem(i, 0, QTableWidgetItem(item[0]))
            if last_status == "NODATA":
                print(f"no data for {item[0]} in table")
                table_object.setItem(i, 1, QTableWidgetItem("NODATA"))
                table_object.setItem(i, 2, QTableWidgetItem("NODATA"))
                table_object.setItem(i, 3, QTableWidgetItem("NODATA"))
            else:
                table_object.setItem(i, 1, QTableWidgetItem(last_status))
                table_object.setItem(i, 2, QTableWidgetItem(avg_duration_on))
                table_object.setItem(i, 3, QTableWidgetItem(last_duration_on))
            i = i+1

    def display_numerical_status(self, db_name, table_object):
        """displays status of all items in list"""

        # get the user selected time
        start_time = self.ui.dateTimeEdit_start.dateTime()
        now_time = self.ui.dateTimeEdit_end.dateTime()
        date_string_start = self.convert(now_time)
        date_string_end = self.convert(start_time)
        print("from ", date_string_start, " to ", date_string_end)

        # finds all distinct items in the database
        sql_str = f"SELECT DISTINCT(sname) FROM {db_name} ORDER BY sname;"
        item_list = self.executeQuery(sql_str)
        print(item_list)
        list_length = len(item_list)

        # set the table dimensions for the output table
        table_object.setColumnCount(3)
        table_object.setRowCount(list_length)
        table_object.setHorizontalHeaderItem(0,QTableWidgetItem("Item"))
        table_object.setHorizontalHeaderItem(1, QTableWidgetItem("Cur_Status"))
        table_object.setHorizontalHeaderItem(2, QTableWidgetItem("Average"))

        sql_str = f"SELECT sdatetime, sname, smessage FROM {db_name} WHERE sdatetime <= {date_string_end} AND" \
            f" sdatetime >= {date_string_start};"
        # note for the sql_str it might be good to get only a months worth of data
        print(sql_str)
        query_result = self.executeQuery(sql_str)
        query_length = len(query_result)

        print(query_result)
        i = 0

        # this for loop finds every unique sensor in the DB and outputs its smessage to the table
        for item in item_list:
            print(item[0])
            a = query_length
            output = "NODATA"
            count_avg = 0
            total_avg = 0
            # this loop looks backwards from the last datapoint with the currently selected datetime and
            # finds the last output of each item
            print("while")
            while a > 0:
                # this is before the rest of the code because matrices in python count from 0; so max row is length - 1
                a = a - 1
                print(a)
                if item[0] == query_result[a][1]:
                    print(a)
                    if output == "NODATA":
                        output = query_result[a][2]
                        print(output)
                    total_avg = total_avg + int(query_result[a][2])
                    count_avg = count_avg + 1

            if count_avg > 0:
                avg = round(total_avg/count_avg,2)
            else:
                avg = "NODATA"
            print(avg)
            table_object.setItem(i, 0, QTableWidgetItem(item[0]))
            table_object.setItem(i, 1, QTableWidgetItem(output))
            table_object.setItem(i, 2, QTableWidgetItem(str(avg)))
            i = i+1

    def display_door(self):
        """displays the status of all the doors in the building"""
        db_name = "door"
        table_object = self.ui.doorTable
        string_bool = ["CLOSE", "OPEN"]

        self.display_binary_status(db_name, table_object, string_bool)

    def display_fan(self):
        """displays the status of all the fans in the building"""
        db_name = "fan"
        table_object = self.ui.fanTable
        string_bool = ["OFF", "ON"]
        self.display_binary_status(db_name, table_object, string_bool)

    def display_item(self):
        """displays the status of all the items in the building"""
        db_name = "item"
        table_object = self.ui.itemTable
        string_bool = ["ABSENT", "PRESENT"]
        self.display_binary_status(db_name, table_object, string_bool)


    def display_motion(self):
        """displays the status of all the motion sensors in the building"""
        db_name = "motion"
        table_object = self.ui.motionTable
        string_bool = ["OFF", "ON"]
        self.display_binary_status(db_name, table_object, string_bool)

    def display_light(self):
        """displays the status of all the lights in the building"""
        db_name = "light"
        table_object = self.ui.lightTable
        self.display_numerical_status(db_name, table_object)

    def display_temp(self):
        """displays the status of all the temperature sensors in the building"""
        db_name = "temp"
        table_object = self.ui.tempTable
        self.display_numerical_status(db_name, table_object)

    def display_batt(self):
        """displays the status of all the battery voltages in the building"""
        db_name = "battPerc"
        table_object = self.ui.battTable
        list_object = self.ui.battList
        self.display_battery_status(db_name, table_object, list_object)

    def display_lightswitch(self):
        """displays the system information"""
        db_name = "l"
        table_object = self.ui.lightswitchTable
        string_bool = ["OFF", "ON"]
        self.display_binary_status(db_name, table_object, string_bool)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = outputGUI()
    window.show()
    sys.exit(app.exec_())
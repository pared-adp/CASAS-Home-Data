import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "datetime_list_01.ui" # Enter designer file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class output_gui(QMainWindow):
    def __init__(self):
        super(output_gui, self).__init__()
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
        self.ui.pushButton_refresh_system.clicked.connect(self.display_system)


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

    def display_status_old(self, db_name, table_object):
        """DEPRECATED used for comparison testing"""

        #get the user selected time
        now_time = self.ui.dateTimeEdit.dateTime()
        date_string = self.convert(now_time)
        print(date_string)

        #finds all distinct items in the database
        sql_str = f"SELECT DISTINCT(sname) FROM {db_name} ORDER BY sname"
        item_list = self.executeQuery(sql_str)
        print(item_list)
        list_length = len(item_list)

        #set the table demensions for the output table
        table_object.setColumnCount(2)
        table_object.setRowCount(list_length)

        print(list_length)
        i = 0
        # this for loop queries finds every unique sensor in the DB and outputs its smessage to the table
        for item in item_list:
            print(item[0])
            sql_str = f"SELECT sname, smessage FROM {db_name} WHERE sdatetime = (SELECT MAX(sdatetime) " \
                f"FROM {db_name} WHERE sname = '{item[0]}' AND sdatetime <= {date_string})"
            print(sql_str)
            query_result = self.executeQuery(sql_str)
            print(query_result)
            if len(query_result) != 0:
                table_object.setItem(i, 0, QTableWidgetItem(query_result[0][0]))
                table_object.setItem(i, 1, QTableWidgetItem(query_result[0][1]))
            else:
                table_object.setItem(i, 0, QTableWidgetItem(item[0]))
                table_object.setItem(i, 1, QTableWidgetItem("NODATA"))
            i= i+1

    def display_status(self, db_name, table_object):
        """displays status of all items in list"""

        #get the user selected time
        now_time = self.ui.dateTimeEdit.dateTime()
        date_string = self.convert(now_time)
        print(date_string)

        #finds all distinct items in the database
        sql_str = f"SELECT DISTINCT(sname) FROM {db_name} ORDER BY sname;"
        item_list = self.executeQuery(sql_str)
        print(item_list)
        list_length = len(item_list)

        # set the table demensions for the output table
        table_object.setColumnCount(2)
        table_object.setRowCount(list_length)

        sql_str = f"SELECT sdatetime, sname, smessage FROM {db_name} WHERE sdatetime <= {date_string};"
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
            # this loop looks backwards from the last datapoint with the currently selected datetime and
            # finds the last output of each
            while a > 0:
                # this is before the rest of the code because matrices in python count from 0; so max row is length - 1
                a = a - 1
                if item[0] == query_result[a][1]:
                    print(a)
                    output = query_result[a][2]
                    print(output)
                    table_object.setItem(i, 0, QTableWidgetItem(item[0]))
                    table_object.setItem(i, 1, QTableWidgetItem(output))
                    break
            else:
                table_object.setItem(i, 0, QTableWidgetItem(item[0]))
                table_object.setItem(i, 1, QTableWidgetItem("NODATA"))

            i= i+1

    def display_door(self):
        """displays the status of all the doors in the building"""
        db_name = "door"
        table_object = self.ui.doorTable
        self.display_status(db_name,table_object)

    def display_fan(self):
        """displays the status of all the fans in the building"""
        db_name = "fan"
        table_object = self.ui.fanTable
        self.display_status(db_name,table_object)

    def display_item(self):
        """displays the status of all the items in the building"""
        db_name = "item"
        table_object = self.ui.itemTable
        self.display_status(db_name,table_object)

    def display_motion(self):
        """displays the status of all the motion sensors in the building"""
        db_name = "motion"
        table_object = self.ui.motionTable
        self.display_status(db_name,table_object)

    def display_light(self):
        """displays the status of all the lights in the building"""
        db_name = "light"
        table_object = self.ui.lightTable
        self.display_status(db_name,table_object)

    def display_temp(self):
        """displays the status of all the temperature sensors in the building"""
        db_name = "temp"
        table_object = self.ui.tempTable
        self.display_status(db_name,table_object)

    def display_batt(self):
        """displays the status of all the battery voltages in the building"""
        db_name = "battvolt"
        table_object = self.ui.battTable
        self.display_status(db_name,table_object)

    def display_system(self):
        """displays the system information"""
        db_name = "system"
        table_object = self.ui.systemTable
        self.display_status(db_name,table_object)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = output_gui()
    window.show()
    sys.exit(app.exec_())

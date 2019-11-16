import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "datetime_list.ui" # Enter designer file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class output_gui(QMainWindow):
    def __init__(self):
        super(output_gui, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #all butuons/user inputs should be initialized here
        self.ui.pushButton_refresh.clicked.connect(self.display_status)

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

    def display_status(self):
        """displays whether the last door was open or closed"""
        now_time = self.ui.dateTimeEdit.dateTime()
        date_string = self.convert(now_time)
        print(date_string)

        sql_str = f"SELECT sname, smessage FROM door WHERE sdatetime = (SELECT MAX(sdatetime) FROM door WHERE" \
            f" sdatetime <= {date_string})"

        print(sql_str)
        query_results = self.executeQuery(sql_str)

        print(query_results)
        print(query_results[0][0])

        #outputs whether the last door was open or closed
        #example of the type of output for the final display
        self.ui.doorTable.setColumnCount(2)
        self.ui.doorTable.setRowCount(1)
        self.ui.doorTable.setItem(0, 0, QTableWidgetItem(query_results[0][0]))
        self.ui.doorTable.setItem(0, 1, QTableWidgetItem(query_results[0][1]))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = output_gui()
    window.show()
    sys.exit(app.exec_())

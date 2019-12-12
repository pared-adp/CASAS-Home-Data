import pandas as pd
from sklearn.neural_network import MLPClassifier
import psycopg2
from datetime import datetime
import numpy as np
from postgre_conn import executeQuery


def main():
    sql_str = "SELECT sdatetime, sname, smessage FROM Door UNION SELECT sdatetime, sname, smessage FROM fan UNION " \
              "SELECT sdatetime, sname, smessage FROM L UNION SELECT sdatetime, sname, smessage FROM item UNION " \
              "SELECT sdatetime, sname, smessage FROM Motion"
    print(sql_str)
    query_result = executeQuery(sql_str)

    qr_df = pd.DataFrame(query_result, columns=["Date Time", "Sensor", "Message",])
    #print(qr_df)

    win_indx = 0
    start = 0
    sensorNames = qr_df.Sensor.unique()
    sensorNames = sensorNames + 'Window Length' + 'Time Difference' + 'Label'
    feature = pd.DataFrame(columns=sensorNames)
    window = 100
    date_str = '%Y-%m-%d %H:%M:%S.%f'
    diff = []
    time = []

    for row in range(0, len(qr_df)):
        print(win_indx)
        if (row + 1) % window == 0:
            test = qr_df.iloc[win_indx:row]
            p1 = test['Sensor'].value_counts()  # sensor count features
            feature = feature.append(p1, ignore_index=True)

            time1 = str(test['Date Time'].iat[0])  # converts to datetime structures to find difference
            time2 = str(test['Date Time'].iat[-1])
            d1 = datetime.strptime(time1, date_str)
            d2 = datetime.strptime(time2, date_str)
            diff.append(int((d2 - d1).total_seconds() / 60))
            time.append(time1)
            win_indx += window

    # generating additional feature values
    feature['Datetime'] = np.array(time)
    feature['Time Difference'] = np.array(diff)
    feature['Window Length'] = len(test)
    feature.replace(np.nan, 0, inplace=True)
    feature.to_csv('feature_test.csv')

main()

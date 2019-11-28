import psycopg2
from datetime import datetime
from dateutil import parser
from datetime import timedelta

"""
This is how I populated the battDrainRate table. This will not run if you don't run the (DELETE FROM BattDrainRate)
command in SQL first. which is fine if you want to test, the code doesn't take too long to run. I believe that some
of these batteries are either solar or are connected to power, that's why they have such a low drain rate. Drain rate
units are percentage of battery / days; so how much percentage of battery is lost each day.
"""


def executeQuery(sql_str):
    """executes an sql query"""
    try:
        conn = psycopg2.connect(
            "dbname='smarthome' user='postgres' host='smarthome.csjinfsewgpk.us-east-2.rds.amazonaws.com' password='12345678'")
    except:
        print('Unable to connect to database')
    cur = conn.cursor()
    cur.execute(sql_str)
    conn.commit()
    result = cur.fetchall()

    return result


def pushQuery(sql_str):
    """pushes data to sql database"""
    try:
        conn = psycopg2.connect(
            "dbname='smarthome' user='postgres' host='smarthome.csjinfsewgpk.us-east-2.rds.amazonaws.com' password='12345678'")
    except:
        print('Unable to connect to database')
    cur = conn.cursor()
    cur.execute(sql_str)
    conn.commit()
    conn.close()

# finds all distinct items in the database
sql_str = f"SELECT DISTINCT(name) FROM battperc ORDER BY name;"
item_list = executeQuery(sql_str)
print(item_list)
list_length = len(item_list)

sql_str = f"SELECT sdatetime, name, message FROM battperc;"
# note for the sql_str it might be good to get only a months worth of data
print(sql_str)
query_result = executeQuery(sql_str)
query_length = len(query_result)

print(query_result)
i = 0

# this for loop finds every unique sensor in the DB and outputs its smessage to the table
for item in item_list:
    print(item[0])
    a = query_length
    current_level = None
    current_time = None
    last_level = None
    last_time = None
    first_charge_level = None
    first_charge_time = None
    final_charge_level = None
    final_charge_time = None
    count_pd = 0

    while a > 0:
        # this is before the rest of the code because matrices in python count from 0; so max row is length - 1
        a = a - 1
        if item[0] == query_result[a][1]:
            current_level = float(query_result[a][2])
            if final_charge_level is None:
                if current_level <= 95: # this makes the final_charge level useful for calculation
                    #set first final charge
                    final_charge_level = float(query_result[a][2])
                    final_charge_time = parser.parse(query_result[a][0])
                    print(f"initial final level and time {final_charge_level}, {final_charge_time}")
            # checks if there is a manual battery change
            elif last_level > current_level + 10: # the 10 prevents variation in data be read as a battery change
                # resets the first charge level to the last level after charge
                first_charge_level = last_level
                first_charge_time = last_time
                print(f"first level and time {first_charge_level}, {first_charge_time}")
                print(f"final level and time {final_charge_level}, {final_charge_time}")

                if (final_charge_time-first_charge_time).total_seconds() > 0:
                    # finds the power_drain from the most recent first charge and the next (chronologically) final charge
                    power_drain = power_drain + \
                                  (first_charge_level - final_charge_level)/(final_charge_time-first_charge_time).total_seconds()
                    count_pd = count_pd + 1
                    print(f"power drain {power_drain} perc/sec")

                #resets the final charge and time for the next power_drain caluclation
                final_charge_level = current_level
                final_charge_time = parser.parse(query_result[a][0])

            # saves the last charge and time for the next loop
            last_level = float(query_result[a][2])
            last_time = parser.parse(query_result[a][0])

    # sets last first charge and time
    # this is done because some batteries are not changed manually in our dataset therefore the calculation will be done
    # from the first charge and time, and the final charge and time in the dataset
    first_charge_level = last_level
    first_charge_time = last_time
    # checks if there is sufficient data to calculate the power_drain
    if final_charge_level is None:
        avg_power_drain = "NULL"
    # if calculations are usefull the this will find the avg power drain
    elif final_charge_time != first_charge_time:
        power_drain = (first_charge_level - final_charge_level) / (final_charge_time - first_charge_time).total_seconds()
        count_pd = count_pd + 1
        avg_power_drain = (power_drain / count_pd)*60*60*24
    else:
        avg_power_drain = "NULL"
    print(f"{item[0]}total power drain {avg_power_drain} perc/day")
    # pushes the item and drainrate to the database
    sql_str = f"INSERT INTO BattDrainRate(battID, drainRate) VALUES ('{item[0]}',{avg_power_drain});"
    pushQuery(sql_str)

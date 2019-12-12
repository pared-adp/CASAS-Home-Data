import psycopg2


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
    conn.close()
    return result
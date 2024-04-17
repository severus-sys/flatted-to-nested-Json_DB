import json
import psycopg2
from psycopg2 import extras
import conf
from datetime import datetime
import sys

try:
    conn = psycopg2.connect(
        dbname=conf.dbname,
        user=conf.user,
        password=conf.password,
        host=conf.host,
        port=conf.port,
    )
    cur = conn.cursor()

except:
    print("Connection Configuration Error")
    sys.exit()


# take data variable from conf pyhton file
data = conf.data


# this function convert string value to timestamp type for timestamp value
def string_to_timestamp(ts_str):
    return datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%S.%fZ")


def insert_to_timestamp_table():
    # get unique values of timestamps
    # because there are timestamp table and unique
    # inserting data to timestamp table
    timestamps = set(string_to_timestamp(item["timestamp"]) for item in data)
    # executemany functions  needs a list as like parametre  parametre olarak bir liste bekler ve bu listedeki her bir öğe bir tuple olmalıdır
    timestamp_data = [(t,) for t in timestamps]
    cur.executemany(
        'INSERT INTO public."Timestamps" (timestamp) VALUES (%s) ON CONFLICT (timestamp) DO NOTHING',
        timestamp_data,
    )
    conn.commit()


def insert_to_variables_table():
    """
    insert data  to variable table
    """
    variables = set()
    for item in data:
        for key in item.keys():
            if key not in ["timestamp", "time_point"]:
                variables.add(key)

    variable_data = [(v,) for v in variables]
    cur.executemany(
        'INSERT INTO public."Variables" (name) VALUES (%s) ON CONFLICT (name) DO NOTHING',
        variable_data,
    )
    conn.commit()


def insert_to_values():
    """
    insert data  to values table
    """
    values = set()
    for item in data:
        for key, value in item.items():
            if key not in ["timestamp", "time_point"]:
                values.add(value)
    value_data = [(v,) for v in values]

    cur.executemany(
        'INSERT INTO public."Values" (value) VALUES (%s) ON CONFLICT (value) DO NOTHING',
        value_data,
    )
    conn.commit()


def insert_to_measurements_table():
    "insert  data to measurements table"
    try:
        cur.execute('SELECT id, timestamp FROM public."Timestamps"')
        timestamp_ids = {row[1]: row[0] for row in cur.fetchall()}
    except Exception as e:
        print("Timestamp table access error")
        print(e)
    for item in data:
        timestamp = string_to_timestamp(item["timestamp"])
        timestamp_id = timestamp_ids[timestamp]
        time_point = item["time_point"]
        cur.execute(
            """
            INSERT INTO public."Measurements"
            (time_point, timestamp_id) VALUES (%s, %s)""",
            (time_point, timestamp_id),
        )
    conn.commit()


def insert_to_measurements_values():
    # insert data to  measurements_value table
    try:
        cur.execute('SELECT id FROM public."Measurements"')
        measurement_ids = [row[0] for row in cur.fetchall()]

        cur.execute('SELECT id, name FROM public."Variables"')
        variable_ids = {row[1]: row[0] for row in cur.fetchall()}

        cur.execute('SELECT id, value FROM public."Values"')
        value_ids = {row[1]: row[0] for row in cur.fetchall()}

    except Exception as e:
        print("Data not found")
        print(e)

    etl_date = datetime.now()

    for measurement_id, item in zip(measurement_ids, data):
        for key, value in item.items():
            if key not in ["timestamp", "time_point"]:
                variable_id = variable_ids[key]
                value_id = value_ids[value]
                cur.execute(
                    """INSERT INTO public."Measurement_Values" 
                    (measurement_id, variable_id, value_id, etl_date) 
                    VALUES (%s, %s, %s, %s)""",
                    (measurement_id, variable_id, value_id, etl_date),
                )
    conn.commit()


insert_to_timestamp_table()
insert_to_variables_table()
insert_to_values()
insert_to_measurements_table()
insert_to_measurements_values()

conn.close()

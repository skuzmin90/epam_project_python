import sys
import os
import time
import requests
import psycopg2
import calendar
from datetime import datetime
from joblib import Parallel, delayed
from flask import Flask, render_template, request, jsonify

city_id = requests.get("https://www.metaweather.com/api/location/search/?query={}".format('Moscow')).json()[0]['woeid']
num_days = calendar.monthrange(datetime.now().year, datetime.now().month)[1]
days = [('{:04}/{:02}/{:02}/'.format(datetime.now().year, datetime.now().month, day)) for day in range(1, num_days + 1)]
column_names = ["id", "weather_state_name", "wind_direction_compass", "created",
                    "applicable_date", "min_temp", "max_temp", "the_temp"]

db_params = {
    "host": os.getenv('DB_HOST'),
    "database": os.getenv('DB_NAME'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "port": "5432"
}

# db_params = {
#     "host": "192.168.208.138",
#     "database": "postgres",
#     "user": "epam",
#     "password": "SSpassword",
#     "port": "5432"
# }

def get_weather_result(city_id, date):
    url = "https://www.metaweather.com/api/location/{}/{}".format(city_id, date)
    weather_result = requests.get(url)
    return weather_result.json()

def connect(db_params):
    conn = None
    try:
        # print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**db_params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    # print("Connection successful")
    return conn

def insert_table():
    try:
        conn = connect(db_params)
        cursor = conn.cursor()
        cursor.execute(""" CREATE TABLE IF NOT EXISTS forecast (id bigint UNIQUE, weather_state_name varchar(45),\
            wind_direction_compass varchar(45), created varchar(45), applicable_date varchar(45), min_temp integer,\
            max_temp integer, the_temp integer); """)
        for date in days:
            result = get_weather_result(city_id, date)
            for item in result:
                sql = """ INSERT INTO forecast VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING; """
                table_data = [item[column] for column in column_names]
                cursor.execute(sql, table_data)
                conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Failed inserting record into mobile table {}".format(error))
    cursor.close()
    conn.close()

def postgresql_query(conn, select_query):
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    res = cursor.fetchall()
    cursor.close()
    return res

def worker(i):
    print('worker ', i)
    x = 0
    while x < 1000:
        print(x)
        x += 1

insert_table()

list_of_date = [item[0] for item in postgresql_query(conn=connect(db_params),
                                                         select_query="""SELECT DISTINCT(applicable_date)"
                                                                 " FROM forecast ORDER BY applicable_date;""")]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',list_of_date=list_of_date)

@app.route('/results', methods=['POST','GET'])
def results():
    select = request.form.get('date_select')
    conn = connect(db_params)
    sql_query = """ SELECT * FROM forecast WHERE applicable_date = '{}' ORDER BY created; """.format(select)
    date_weather = postgresql_query(conn, sql_query)
    conn.close()
    return render_template('results.html', select=select, list_of_date=list_of_date, date_weather=date_weather)

@app.route('/update', methods=['POST','GET'])
def update():
    insert_table()
    return render_template('update.html', list_of_date=list_of_date)

@app.route('/stress')
def myfunc():
    start_time = time.time()
    Parallel(n_jobs=-1, prefer="processes", verbose=0)(
            delayed(worker)(num)
            for num in range(12000)
    )
    end_time = time.time() - start_time
    resp = jsonify(success=True, time=str(end_time))
    resp.status_code = 200
    return resp

if __name__ == '__main__':
     app.run()
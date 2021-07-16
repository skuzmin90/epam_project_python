import requests
import psycopg2
import calendar
from datetime import datetime
from flask import Flask, render_template,request

def get_city_id(city_name):
    url_city = "https://www.metaweather.com/api/location/search/?query={}".format(city_name)
    return requests.get(url_city).json()[0]['woeid']

def get_weather_result(city_id, date):
    url = "https://www.metaweather.com/api/location/{}/{}".format(city_id, date)
    weather_result = requests.get(url)
    return weather_result.json()

db_params = {
    "host": '192.168.208.138',
    "database": "weather",
    "user": "postgres",
    "port": "5432"
}

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

def tableInsert(item):
    try:
        conn = connect(db_params)
        cursor = conn.cursor()
        table_data = [item[column] for column in column_names]
        sql = """ INSERT INTO weather VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING """
        cursor.execute(sql, tuple(table_data))
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Failed inserting record into mobile table {}".format(error))
    finally:
        if conn:
            cursor.close()
            conn.close()
            # print("PostgreSQL connection is closed")

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

num_days = calendar.monthrange(datetime.now().year, datetime.now().month)[1]
days = [('{:04}/{:02}/{:02}/'.format(datetime.now().year, datetime.now().month, day)) for day in range(1, num_days + 1)]

column_names = ["id", "weather_state_name", "wind_direction_compass", "created",
                    "applicable_date", "min_temp", "max_temp", "the_temp"]

for date in days:
    result = get_weather_result(get_city_id('Moscow'), date)
    for item in result:
        tableInsert(item)

list_of_date = [item[0] for item in postgresql_query(conn=connect(db_params),
                                                         select_query="""SELECT DISTINCT(applicable_date)"
                                                         " FROM weather ORDER BY applicable_date;""")]

def update_table():
    for date in days:
        result = get_weather_result(get_city_id('Moscow'), date)
        for item in result:
            tableInsert(item)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',list_of_date=list_of_date)

@app.route('/results', methods=['GET', 'POST'])
def render_results():
    select = request.form['date_select']
    conn = connect(db_params)
    sql_query = """SELECT * FROM weather WHERE applicable_date = '{}' ORDER BY created;""".format(select)
    date_weather = postgresql_query(conn, sql_query)
    conn.close()
    return render_template("results.html", select=select, date_weather=date_weather, list_of_date=list_of_date)

@app.route('/update', methods=['GET', 'POST'])
def update():

    return render_template('results.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    conn = connect(db_params)
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM weather;""")
    conn.commit()
    conn.close()
    return render_template('delete.html')

if __name__ == '__main__':
     app.run()
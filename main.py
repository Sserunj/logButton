from flask import Flask, request, jsonify,json
import mysql.connector
from flask_cors import CORS
import datetime
app = Flask(__name__)
CORS(app)

# Database configuration
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
}

# create mysql connection
db_connect = mysql.connector.connect(**db_config)

db_cursor = db_connect.cursor()

# create database if not exists
db_cursor.execute('''CREATE DATABASE IF NOT EXISTS farm''')
db_connect.commit()
db_cursor.close()


@app.route('/log', methods=['POST'])
def log_date_time():
    if request.method == 'POST':
        name = request.args.get('name')
        current_datetime = datetime.datetime.now()
        date = current_datetime.strftime('%a %d %b %Y')
        time = current_datetime.strftime('%I:%M:%p')
        data = {
            "Name": name,
            "Date": date,
            "Time": time
        }
        db_cursor = db_connect.cursor()
        db_cursor.execute('''USE farm''')
        db_cursor.execute('''CREATE TABLE IF NOT EXISTS logs (name VARCHAR(50),date VARCHAR(50), time VARCHAR(50))''')
        db_cursor.execute(''' INSERT INTO logs VALUES(%s,%s,%s)''',(name,date,time))
        db_connect.commit()
        db_cursor.close()
        print(data)
        print(type(data))
        return jsonify(data, "Datetime logged")
    return 'Failed to log date and time'

@app.route('/all_logs', methods=['GET'])
def get_date_time():
    if request.method == 'GET':
        db_cursor = db_connect.cursor()
        db_cursor.execute('''USE farm''')
        db_cursor.execute('''SELECT name, date, time FROM logs ORDER BY time DESC''')
        data = db_cursor.fetchall()
        data_dict = [{'name':item[0], 'date':item[1], 'time':item[2]} for item in data]
        json_data = json.dumps(data_dict,indent = 1)
        return json_data
    return 'Failed fetch data from database'


if __name__ == '__main__':
    app.run(debug=True)

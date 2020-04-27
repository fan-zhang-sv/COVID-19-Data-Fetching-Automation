from flask import Flask
# from flask_cors import CORS
import pymysql

import json
app = Flask(__name__)
# CORS(app)


@app.route('/data')
def get_data():
    db = pymysql.connect("localhost", "root", "123456", "covid19")
    cursor = db.cursor()
    sql = "SELECT * FROM DATA"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        output = []
        for row in results:
            temp = {}
            temp['area'] = row[0]
            temp['lat'] = float(row[1])
            temp['lng'] = float(row[2])
            temp['confirmed'] = row[3]
            temp['deaths'] = row[4]
            output.append(temp)
        json_output = json.dumps(output)
        return json_output
    except Exception as e:
        return json.dumps([str(e)])
    db.close()

    # with open('/home/ubuntu/wuhan_flu/api/data.json') as f:
    #     data = json.load(f)
    # output = json.dumps(data)
    # return output


@app.route('/list_data')
def get_list_data():
    db = pymysql.connect("localhost", "root", "123456", "covid19")
    cursor = db.cursor()
    sql = "SELECT * FROM LIST"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        output = []
        for row in results:
            temp = {}
            temp['state'] = row[0]
            temp['confirmed'] = row[1]
            temp['deaths'] = row[2]
            output.append(temp)
        json_output = json.dumps(output)
        return json_output
    except Exception as e:
        return json.dumps([str(e)])
    db.close()
    # with open('/home/ubuntu/wuhan_flu/api/list_data.json') as f:
    #     data = json.load(f)
    # output = json.dumps(data)
    # return output

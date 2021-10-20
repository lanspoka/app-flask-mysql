from flask_cors import CORS
from flask import Flask, jsonify, make_response, send_from_directory
import MySQLdb
#import os
#import json


app = Flask(__name__, static_url_path='/')
cors = CORS(app)


@app.route('/')
def hello():
    return "<h1>Sveiki!</h1>"


@app.route('/static/<path:path_variable>')
def send_js(path_variable):
    return send_from_directory('./HTML/', path_variable)


@app.route("/select")
def select():
    db = MySQLdb.connect("*host*", "*user*", "*passw*", "*database*")
    cur = db.cursor()
    query = "SELECT * FROM artists WHERE ArtistId >= 1 AND ArtistId <= 10"
    cur.execute(query)
    json_data = cur.fetchall()
    cur.close()
    print("json_data (select):")
    print(json_data)
    return jsonify(data=json_data)


@app.route("/select/<int:id>")
def select_by_id(id):
    db = MySQLdb.connect("*host*", "*user*", "*passw*", "*database*")
    cur = db.cursor()
    query = "SELECT * FROM artists WHERE ArtistId=" + str(id)
    cur.execute(query)
    json_data = cur.fetchall()
    cur.close()
    print("json_data (select):")
    print(json_data)
    return jsonify(data=json_data)


@app.route("/get_customer/<int:id>", methods=['GET'])
def get_customer(id):
    db = MySQLdb.connect("*host*", "*user*", "*passw*", "*database*")
    cur = db.cursor()
    proc = "get_customer"
    cur.callproc(proc, [id])

    columns = [x[0] for x in cur.description]
    print(columns)

    data = cur.fetchall()
    print(data)
    json_data = []
    for result in data:
        json_data.append(dict(zip(columns, result)))
        print(json_data)
    cur.close()
    print("json_data (proc):")
    print(json_data)
    response = {'data': json_data}
    return jsonify(data=json_data)


@app.route("/delete_albums/<int:id>", methods=['DELETE'])
def delete_albums(id):
    db = MySQLdb.connect("*host*", "*user*", "*passw*", "*database*")
    cur = db.cursor()
    proc = "delete_albums"
    cur.callproc(proc, [id])
    return "Okey"


if __name__ == '__main__':
    app.run(port=5000)

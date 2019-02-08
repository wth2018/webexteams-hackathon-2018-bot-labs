import sqlite3
from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

def initDatabase():
	conn = sqlite3.connect('about.db')
	cur = conn.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS person (id INTEGER PRIMARY KEY, name VARCHAR(100), age INTEGER)")
	conn.commit()

def fetchDataFromDatabase():
	with sqlite3.connect('about.db') as con:
		cur = con.cursor()
		result = cur.execute("SELECT * FROM person ORDER BY id DESC;").fetchone()
		return jsonify(id = result[0], name = result[1], age = result[2])

def pushDataToDatabase(name, age):
	with sqlite3.connect('about.db') as con:
		cur = con.cursor()
		sql = f"INSERT INTO person (name, age) VALUES ('{name}', {age});"
		cur.execute(sql)
		con.commit()

static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')

@app.route("/")
def index():  
	return app.send_static_file('index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_static_dir(path):
	return send_from_directory(static_file_dir, path)

@app.route("/api/helloworld")
def hello():
  return "Hello World!"

@app.route("/api/about", methods = ['POST', 'GET'])
def about():
	if request.method == 'GET':
		return fetchDataFromDatabase()
	elif request.method == 'POST':
		r = request.json
		name = r["name"]
		age = r["age"]
		pushDataToDatabase(name, age)
		return jsonify(name = name, age = age)


initDatabase()
pushDataToDatabase("Charles Webex", 15)
app.run()
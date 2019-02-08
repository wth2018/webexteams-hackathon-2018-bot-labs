from flask import Flask, jsonify, request
app = Flask(__name__)

name = "Charles Webex" 
age = "15"

@app.route("/api/helloworld")
def hello():
  return "Hello World!"

@app.route("/api/about", methods = ['POST', 'GET'])
def about():
	global name, age
	if request.method == 'GET':
		return jsonify(name = name, age = age)
	elif request.method == 'POST':
		r = request.json
		name = r["name"]
		age = r["age"]
		return jsonify(name = name, age = age)

app.run()
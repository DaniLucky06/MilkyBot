from flask import Flask, request, jsonify
from threading import Thread
import json
app = Flask(__name__)

@app.route('/get-user-info', methods=['GET'])
def home():
  f = open("./data/users.json", "r").read()
  print(f)
  return jsonify(json.loads(f))
def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
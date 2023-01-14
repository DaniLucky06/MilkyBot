from flask import Flask, request, jsonify
from threading import Thread
app = Flask(__name__)

@app.route('/get-user-info', methods=['GET'])
def home():
  if request.headers.get('request-user-info', "none") == "none":
    return jsonify({
      "success": False,
      "message": "Insufficient Headers: request-user-info missing"
    })
  else:
    try:
      user = request.headers.get('request-user-info', "none")
      print(user)
      return jsonify({
      "success": True,
      "user": {
        "name": request.headers.get('request-user-info', "none"),
        "avatar": "https://cdn.discord.com/shitAvatar",
        "status": "online"
      }
    })
    except:
      return jsonify({ 
        "success": False
      })

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
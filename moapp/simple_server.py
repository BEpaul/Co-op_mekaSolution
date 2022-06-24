#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 13:33:24 2022
@author: hsherlcok
"""

from flask import Flask
from flask import request
from flask import jsonify

# This line is for solving flask's CORS error
# You need 'pip install flask_cors' to use flask_cors
#from flask_cors import CORS
from werkzeug.serving import WSGIRequestHandler
import json
WSGIRequestHandler.protocol_version = "HTTP/1.1"

app = Flask(__name__)

# This line is for solving flask's CORS error
#CORS(app)

global users
users = []

@app.route("/getuser", methods=['GET'])
def get_name():
    name = request.args.get('name')
    
    global users
    exist = False
    ret = {}
    for usr in users:
        if usr[0] == name:
            ret["username"] = usr[0]
            ret["age"] = usr[1]
            
            exist = True
            break
    
    # return jsonify(maze=string.decode('utf-8', 'ignore'))
    return jsonify (ret)

@app.route("/adduser", methods=['POST'])
def update_name():
    content = request.get_json(silent=True)
    
    username = content["username"]
    age = content["age"]

    global users
    exist = False
    for usr in users:
        if usr[0] == username:
            exist = True

    if exist is False:
        users.append ([username, age])
        return jsonify(success=True)
    else:
        return jsonify(success=False)
    
if __name__ == "__main__":
    app.run(host='localhost', port=8888)
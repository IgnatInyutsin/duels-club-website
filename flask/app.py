import os
from flask import Flask, jsonify, request, Response
import migrations, getData
import json

app = Flask(__name__)

@app.route('/migrations')
def migration():
    migrations.main()
    resp = Response("Complete!")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/add_result')
def addResult():
    resp = Response("None")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/add_session')
def addSession():
    resp = Response("None")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/get_data', methods=['GET'])
def get_data():
    resp = Response(json.dumps(getData.main(request.args['sql']), sort_keys=True, indent=2, ensure_ascii=False, default=str))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0')
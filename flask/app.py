import os
from flask import Flask, jsonify, request, Response
import migrations, getData, addData, getResult, addUser, createInvite
import json

app = Flask(__name__)

# Обработка запросов на разные адреса
@app.route('/api/migrations')
def migration():
    # Запускаем миграцию
    migrations.main()
    resp = Response("Complete!")
    #Ставим заголовки
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/api/add_data')
def addResult():
    resp = Response(json.dumps(addData.main(request.args['sql']), sort_keys=True, indent=2, ensure_ascii=False, default=str))
    #Ставим заголовки
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/api/get_data', methods=['GET'])
def get_data():
    #Результат функции делаем json
    resp = Response(json.dumps(getData.main(request.args['sql']), sort_keys=True, indent=2, ensure_ascii=False, default=str))
    #Ставим заголовки
    resp.headers['Content-Type'] = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/api/get_result', methods=['GET'])
def get_result():
    #Результат функции делаем json
    resp = Response(json.dumps(getResult.main(request.args['myID'], request.args['opponentNick'], request.args['gameResult'], request.args['gameComment']), sort_keys=True, indent=2, ensure_ascii=False, default=str))
    #Ставим заголовки
    resp.headers['Content-Type'] = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/api/add_user', methods=['GET'])
def add_user():
    #Результат функции делаем str
    resp = Response(addUser.main(request.args['nickname'], request.args['password'], request.args['invite']))
    #Ставим заголовки
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/api/create_invite', methods=['GET'])
def create_invite():
    #Результат функции делаем str
    resp = Response(json.dumps(createInvite.main(), sort_keys=True, indent=2, ensure_ascii=False, default=str))
    #Ставим заголовки
    resp.headers['Content-Type'] = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0')
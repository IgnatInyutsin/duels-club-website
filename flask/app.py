import os
from flask import Flask, jsonify, request, Response
import migrations, getData, addData, getResult
import json

app = Flask(__name__)

# Обработка запросов на разные адреса
@app.route('/migrations')
def migration():
    # Запускаем миграцию
    migrations.main()
    resp = Response("Complete!")
    #Ставим заголовки
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/add_data')
def addResult():
    resp = Response(json.dumps(addData.main(request.args['sql']), sort_keys=True, indent=2, ensure_ascii=False, default=str))
    #Ставим заголовки
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/get_data', methods=['GET'])
def get_data():
    #Результат функции делаем str
    resp = Response(json.dumps(getData.main(request.args['sql']), sort_keys=True, indent=2, ensure_ascii=False, default=str))
    #Ставим заголовки
    resp.headers['Content-Type'] = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/get_result', methods=['GET'])
def get_result():
    #Результат функции делаем str
    resp = Response(json.dumps(getResult.main(request.args['myID'], request.args['opponentNick'], request.args['gameResult'], request.args['gameComment']), sort_keys=True, indent=2, ensure_ascii=False, default=str))
    #Ставим заголовки
    resp.headers['Content-Type'] = "application/json"
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
if __name__ == '__main__':
    app.run(host='0.0.0.0')
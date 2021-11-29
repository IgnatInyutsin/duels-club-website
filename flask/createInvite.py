from flask import Flask, jsonify, request
import app
import database
import uuid

def main():
    #подключаемся к бд
    db = database.init()
    #создаем курсор
    cursor = db.cursor()
    #создаем рандомный id
    randomID = uuid.uuid4().hex

    #добавляю новую строку
    cursor.execute('''
    INSERT INTO invite (invite_id) VALUES ('{}');
    '''.format(randomID))
    #отправляю изменения
    db.commit()

    return {"id": randomID}
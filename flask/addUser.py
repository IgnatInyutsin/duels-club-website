from flask import Flask, jsonify, request
import app
import database

def main(usrNickname, usrPass, inviteID):
    #подключение к дб
    db = database.init()
    #установка курсора
    cursor = db.cursor()
    
    #создаем новую строку в таблице
    cursor.execute('''
    INSERT INTO member (nickname, passcache, wins, defeat, draw, elo, max_elo)
    VALUES ('{}', '{}', 0, 0, 0, 1500, 1500);
    '''.format(usrNickname, usrPass))
    #удаляем приглашение
    cursor.execute('''
    DELETE FROM invite
    WHERE invite_id = '{}';
    '''.format(inviteID))
    #отправляем изменения
    db.commit()

    return "OK"
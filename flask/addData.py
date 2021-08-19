import os
from flask import Flask, jsonify, request
import app
import database
import uuid
import time

def main(data):
	# Подключаемся к БД
	db = database.init()
	#устанавливаем курсор
	cursor = db.cursor()
	# Делаем запрос если в data значение из ветвлений
	if data[:7]=="session":
		#Собираем всех в рейтинге
		cursor.execute('''
			SELECT session.sessionid 
			FROM session
			''')
		records = cursor.fetchall()
		#рандомный хэш
		randHash = uuid.uuid4().hex
		#генерация пока он не будет уникальным
		i = 0
		while i<len(records):
			if records[i][0] == randHash:
				i=0
				randHash = uuid.uuid4().hex
			else:
				i+=1
		#добавление
		cursor.execute('''
			INSERT INTO session (userid, sessionid, created, ended) VALUES ({0}, '{1}', {2}, {3});
		'''.format(data[7:], randHash, int(time.time()), int(time.time()) + 604800))
		
		#отправка
		db.commit()

		return {"session": randHash}

	elif data[:11]=="sess_remove":
		#удаляем сессию
		cursor.execute('''
			DELETE FROM session
			WHERE sessionid = '{}';'''.format(data[11:]))

		db.commit()

		return {"status": "Complete!"}
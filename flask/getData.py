import os
from flask import Flask, jsonify, request
import app
import database
import time

def main(data):
	# Подключаемся к БД
	db = database.init()
	#устанавливаем курсор
	cursor = db.cursor()
	# Делаем запрос если в data значение из ветвлений
	if data=="rating":
		#Собираем всех в рейтинге
		cursor.execute('''
			SELECT member.nickname, member.drp, member.wins,
			member.defeat, member.draw, member.maxdrp, team.name 
			FROM member 
			JOIN team ON member.commandid = team.teamid
			WHERE wins+defeat+draw > 2
			ORDER BY drp DESC, wins+defeat+draw DESC;''')
		records=cursor.fetchall()

		return records

	elif data=="newers":
		cursor.execute('''
			SELECT member.nickname
			FROM member 
			ORDER BY id DESC
			LIMIT 3;''')
		records=cursor.fetchall()

		return records

	elif data=="top3":
		cursor.execute('''
			SELECT member.nickname
			FROM member
			ORDER BY drp DESC
			LIMIT 3;''')
		records=cursor.fetchall()

		return records

	elif data[:5]=="login":
		cursor.execute('''
			SELECT member.passcache, member.id
			FROM member
			WHERE member.nickname = '{}';'''.format(data[5:]))
		records=cursor.fetchall()

		return records

	elif data[:7]=="session":
		#берем данные о просрочке
		cursor.execute('''
			SELECT session.ended, session.userid
			FROM session
			WHERE sessionid = '{}';'''.format(data[7:]))
		records=cursor.fetchall()
		#если просрочилось удаляем и сообщаем что просрочено
		if records[0][0] <= time.time():
			cursor.execute('''
				DELETE FROM session 
				WHERE sessionid = '{}' '''.format(data[7:]))
			db.commit()
			return {"status": "ended"}
		else:
			return {"status": "not_ended", "id": records[0][1]}
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
			SELECT member.nickname, member.elo, member.wins,
			member.defeat, member.draw, member.max_elo
			FROM member 
			ORDER BY elo DESC, wins+defeat+draw DESC;''')
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
			ORDER BY elo DESC
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
			SELECT session.ended, session.user_id, member.nickname
			FROM session
			JOIN member ON session.user_id = member.id
			WHERE session_id = '{}';'''.format(data[7:]))
		records=cursor.fetchall()
		#если просрочилось удаляем и сообщаем что просрочено
		if records[0][0] <= time.time():
			cursor.execute('''
				DELETE FROM session 
				WHERE session_id = '{}' '''.format(data[7:]))
			db.commit()
			return {"status": "ended"}
		else:
			return {"status": "not_ended", "id": [records[0][1], records[0][2]]}

	elif data=="allMember": #собираем все ники
		cursor = db.cursor()

		cursor.execute("SELECT member.nickname FROM member;")
		records=cursor.fetchall()

		return records

	elif data[:9]=="OneMember":
		cursor = db.cursor()
		#забираем из бд необходимые данные об одном участнике
		cursor.execute('''
			SELECT * FROM
				(SELECT ROW_NUMBER() OVER
					(ORDER BY elo DESC, wins+defeat+draw DESC),
				member.elo,
				member.wins,
				member.defeat,
				member.draw
				FROM member)
					AS all_data
				WHERE id = {}
			'''.format(data[9:]))
		records = list(cursor.fetchone())

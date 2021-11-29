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
			member.defeat, member.draw, member.max_elo, member.id
			FROM member 
			ORDER BY elo DESC, wins+defeat+draw DESC;''')
		records=cursor.fetchall()

		return records

	elif data=="newers":
		cursor.execute('''
			SELECT member.nickname, member.id
			FROM member 
			ORDER BY id DESC
			LIMIT 3;''')
		records=cursor.fetchall()

		return records

	elif data=="top3":
		cursor.execute('''
			SELECT member.nickname, member.id
			FROM member
			ORDER BY elo DESC, wins+defeat+draw DESC
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
			SELECT all_data.*, member.nickname FROM
				(SELECT ROW_NUMBER() OVER
					(ORDER BY elo DESC, wins+defeat+draw DESC),
				member.elo,
				member.wins,
				member.defeat,
				member.draw,
				member.id,
				member.max_elo
				FROM member)
					AS all_data
				JOIN member ON all_data.id = member.id
				WHERE all_data.id = {};
			'''.format(data[9:]))
		records = list(cursor.fetchone())

		return records

	elif data=="matchs":
		cursor = db.cursor()
		#забираем из бд данные о матчах
		cursor.execute('''
			SELECT member.nickname, match.result, match.matchID
			FROM match
			JOIN member ON match.first_player_id = member.id
			ORDER BY matchID DESC
			LIMIT 3;''')
		records = list(cursor.fetchall())

		for i in range(len(records)): #добавляем ник второго игрока
			records[i] = list(records[i])
			cursor.execute('''
				SELECT member.nickname
				FROM match
				JOIN member ON match.second_player_id = member.id
				WHERE matchID = {};
				'''.format(records[i][2]))
			record = cursor.fetchone()[0]
			records[i].append(record)

		output = []
		for i in range(len(records)): #создаем массив из строк
			#проверка результата игры
			if records[i][1] == 1:
				str1 = " (победитель) "
				str2 = " (проигравший) "
			elif records[i][1] == 0:
				str2 = " (победитель) "
				str1 = " (проигравший) "
			else:
				str1 = " (ничья) "
				str2 = " (ничья) "


			output.append([records[i][0] + str1 + " vs" + str2 + records[i][3], records[i][2]])

		return output

	elif data=="lastMatch":
		cursor = db.cursor()
		#забираем из бд данные о последнем матче
		cursor.execute('''
			SELECT member.nickname, match.result, match.commentary, match.matchID
			FROM match
			JOIN member ON match.first_player_id = member.id
			ORDER BY matchID DESC
			LIMIT 1;''')
		record = list(cursor.fetchone())

		#добавляем ник второго игрока
		cursor.execute('''
			SELECT member.nickname
			FROM match
			JOIN member ON match.second_player_id = member.id
			WHERE matchID = {};
			'''.format(record[3]))
		record.append(cursor.fetchone()[0])

		output = [record[2], "", ""]
		#проверка результата игры
		if record[1] == 1:
			str1 = " (победитель) "
			str2 = " (проигравший) "
		elif record[1] == 0:
			str2 = " (победитель) "
			str1 = " (проигравший) "
		else:
			str1 = " (ничья) "
			str2 = " (ничья) "

		#передаем результаты на вывод
		output[1] = record[0] + str1 + " vs" + str2 + record[4]
		output[2] = str(record[3])

		return output

	elif data[:14]=="matchsOfMember":
		cursor = db.cursor()

		#забираем все матчи с участием определенного игрока
		cursor.execute('''
			SELECT match.first_player_id, match.second_player_id, match.matchID
			FROM match
			WHERE first_player_id = {} OR second_player_id = {}
			ORDER BY matchID DESC;
		'''.format(data[14:], data[14:]))

		records = cursor.fetchall()
		output = []

		#проходим по каждой строке отдельно и выполняем действия в соответствии, первый он игрок или второй
		for i in range(len(records)):
			if records[i][0] == int(data[14:]):
				cursor.execute('''
					SELECT match.result, member.nickname, member.id, match.first_player_elo, match.first_elo_change, match.matchID
					FROM match
					JOIN member ON match.second_player_id = member.id
					WHERE first_player_id = {} AND matchID = {};
				'''.format(data[14:], records[i][2]))
				#изменяем результат
				record = cursor.fetchone()
				if record[0] == 1:
					output.append(['Победа'] + list(record[1:]) + ['first'])
				elif record[0] == -1:
					output.append(['Ничья'] + list(record[1:]) + ['first'])
				elif record[0] == 0:
					output.append(['Поражение'] + list(record[1:]) + ['first'])

			elif records[i][1] == int(data[14:]):
				cursor.execute('''
					SELECT match.result, member.nickname, member.id, match.second_player_elo, match.second_elo_change, match.matchID
					FROM match
					JOIN member ON match.first_player_id = member.id
					WHERE second_player_id = {} AND matchID = {};
				'''.format(data[14:], records[i][2]))
				#изменяем результат
				record = cursor.fetchone()
				if record[0] == 1:
					output.append(['Поражение'] + list(record[1:]) + ['first'])
				elif record[0] == -1:
					output.append(['Ничья'] + list(record[1:]) + ['first'])
				elif record[0] == 0:
					output.append(['Победа'] + list(record[1:]) + ['first'])

		return output

	elif data[:16]=="graphicForMember":
		cursor = db.cursor()

		#забираем все изменение рейтинга с начала
		cursor.execute('''
			SELECT match.first_player_elo, match.second_player_elo, match.first_player_id
			FROM match
			WHERE (first_player_id = {}) OR (second_player_id = {})
			ORDER BY matchID ASC;
		'''.format(data[16:], data[16:]))
		records = cursor.fetchall()

		output = [[], ["0 партий"]]
		#сортируем данные
		for i in range(len(records)):
			if records[i][2] == int(data[16:]):
				output[0].append(records[i][0])
			else:
				output[0].append(records[i][1])
			#добавляес номер из числового ряда
			output[1].append(str(i+1) + "парти(я/й)")

		#добавляем в список начальный рейтинг
		output[0] = [1500] + output[0]

		return output

	elif data[:8] == "OneMatch":
		cursor = db.cursor()

		#забираем из бд данные о матче
		cursor.execute('''
			SELECT match.matchID, member.nickname, match.result, match.commentary, match.first_player_elo, match.second_player_elo, match.first_elo_change, match.second_elo_change, member.id
			FROM match
			JOIN member ON match.first_player_id = member.id
			WHERE matchID = {}'''.format(data[8:]))
		record = list(cursor.fetchone())

		#добавляем ник второго игрока
		cursor.execute('''
			SELECT member.nickname, member.id
			FROM match
			JOIN member ON match.second_player_id = member.id
			WHERE matchID = {};
			'''.format(data[8:]))
		record += [cursor.fetchone()[0:]]

		#преобразуем строку результата матча в текст
		if record[2] == 1:
			record[2] = "Победил"
		elif record[2] == 0:
			record[2] = "Проиграл"
		else:
			record[2] = "Ничья"

		return record

	elif data[:8] == "allMatch":
		cursor = db.cursor()

		#забираем из бд данные о матче
		cursor.execute('''
			SELECT match.matchID, member.nickname, match.result, match.commentary, match.first_player_elo, match.second_player_elo, match.first_elo_change, match.second_elo_change, member.id
			FROM match
			JOIN member ON match.first_player_id = member.id;
		''')
		record = list(cursor.fetchall())

		for i in range(len(record)):
			record[i] = list(record[i])

			#добавляем ник второго игрока
			cursor.execute('''
				SELECT member.nickname, member.id
				FROM match
				JOIN member ON match.second_player_id = member.id
				WHERE matchID = {};
			'''.format(record[i][0]))
			record[i] += [cursor.fetchone()]


			#преобразуем строку результата матча в текст
			if record[i][2] == 1:
				record[i][2] = "Победил"
			elif record[i][2] == 0:
				record[i][2] = "Проиграл"
			else:
				record[i][2] = "Ничья"

		return record
	
	elif data[:11] == "checkInvite":
		cursor = db.cursor()

		#проверяем на наличие такого приглашения
		cursor.execute('''
		SELECT * FROM invite
		WHERE invite_id = '{}';
		'''.format(data[11:]))
		
		#проверка на наличие элементов в ответе
		if len(cursor.fetchall()) > 0:
			return {"result": 1}
		else:
			return {"result": 0}
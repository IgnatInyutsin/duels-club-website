import os
from flask import Flask, jsonify, request
import app
import database

def main(myID, opponentNick, gameResult, gameComment):
	# Подключаемся к БД
	db = database.init()
	#устанавливаем курсор
	cursor = db.cursor()

	#забираем из бд данные об игроках
	cursor.execute('''
	SELECT member.id, member.elo, member.max_elo, member.wins, member.defeat, member.draw
	FROM member
	WHERE id = {};
		'''.format(myID))
	oldMyData = cursor.fetchone()

	cursor.execute('''
	SELECT member.id, member.elo, member.max_elo, member.wins, member.defeat, member.draw
	FROM member
	WHERE nickname = '{}';
		'''.format(opponentNick))
	oldOpponentData = cursor.fetchone()

	#массив с измененными данными - копируем в него старый
	newMyData = list(oldMyData)
	newOpponentData = list(oldOpponentData)

	#изменяем параметры
	if gameResult == "win":
		#меняем победы/поражения/ничьи
		newMyData[3] += 1
		newOpponentData[4] += 1

		#изменяем рейтинги игроков
		K = 30 #коэффициент на увеличение/уменьшение рейтинга

		Ea = 1/( 1+10**( (oldOpponentData[1] - oldMyData[1])/400 ) ) #ожидаемый рейтинг игрока 1
		newMyData[1] = round( oldMyData[1] + K * (1 - Ea) ) #новый рейтинг игрока 1

		Eb = 1/( 1+10**( (oldMyData[1] - oldOpponentData[1])/400 ) ) #ожидаемый рейтинг игрока 2
		newOpponentData[1] =  round( oldOpponentData[1] + K * (0 - Eb) ) #новый рейтинг игрока 2

		#Обновляем максимальный рейтинг
		if oldMyData[2] < newMyData[1]:
			newMyData[2] = newMyData[1]

	elif gameResult == "defeat":
		#меняем победы/поражения/ничьи
		newMyData[4] += 1
		newOpponentData[3] += 1

		#изменяем рейтинги игроков
		K = 30 #коэффициент на увеличение/уменьшение рейтинга

		Ea = 1/( 1+10**( (oldOpponentData[1] - oldMyData[1])/400 ) ) #ожидаемый рейтинг игрока 1
		newMyData[1] = round( oldMyData[1] + K * (0 - Ea) ) #новый рейтинг игрока 1

		Eb = 1/( 1+10**( (oldMyData[1] - oldOpponentData[1])/400 ) ) #ожидаемый рейтинг игрока 2
		newOpponentData[1] = round( oldOpponentData[1] + K * (1 - Eb) ) #новый рейтинг игрока 2

		#Обновляем максимальный рейтинг
		if oldOpponentData[2] < newOpponentData[1]:
			newOpponentData[2] = newOpponentData[1]

	elif gameResult == "draw":
		#меняем победы/поражения/ничьи
		newMyData[5] += 1
		newOpponentData[5] += 1

		#изменяем рейтинги игроков
		K = 30 #коэффициент на увеличение/уменьшение рейтинга

		Ea = 1/( 1+10**( (oldOpponentData[1] - oldMyData[1])/400 ) ) #ожидаемый рейтинг игрока 1
		newMyData[1] = round( oldMyData[1] + K * (0.5 - Ea) ) #новый рейтинг игрока 1

		Eb = 1/( 1+10**( (oldMyData[1] - oldOpponentData[1])/400 ) ) #ожидаемый рейтинг игрока 2
		newOpponentData[1] = round( oldOpponentData[1] + K * (0.5 - Eb) ) #новый рейтинг игрока 2

		#Обновляем максимальный рейтинг
		if oldOpponentData[2] < newOpponentData[1]:
			newOpponentData[2] = newOpponentData[1]
		if oldMyData[2] < newMyData[1]:
			newMyData[2] = newMyData[1]

	#обновляем обновленные данные игроков в бд
	cursor.execute('''
		UPDATE member SET wins = {}, defeat = {}, draw = {}, elo = {}, max_elo = {}
		WHERE id = {};
		'''.format(newMyData[3],
			newMyData[4],
			newMyData[5],
			newMyData[1],
			newMyData[2], 
			newMyData[0]))

	cursor.execute('''
		UPDATE member SET wins = {}, defeat = {}, draw = {}, elo = {}, max_elo = {}
		WHERE id = {};
		'''.format(newOpponentData[3],
			newOpponentData[4],
			newOpponentData[5],
			newOpponentData[1],
			newOpponentData[2],
			newOpponentData[0]))

	#добавляем данные о матче в бд
	if gameResult == "win": #если победа
		cursor.execute('''
			INSERT INTO match (result, first_player_id, second_player_id, first_player_elo, second_player_elo, first_elo_change, second_elo_change, commentary)
			VALUES ({}, {}, {}, {}, {}, {}, {}, '{}');
			'''.format( 1,
				newMyData[0],
				newOpponentData[0],
				newMyData[1],
				newOpponentData[1],
				newMyData[1] - oldMyData[1],
				newOpponentData[1] - oldOpponentData[1],
				gameComment ))
	if gameResult == "defeat": #если поражение
		cursor.execute('''
			INSERT INTO match (result, first_player_id, second_player_id, first_player_elo, second_player_elo, first_elo_change, second_elo_change, commentary)
			VALUES ({}, {}, {}, {}, {}, {}, {}, '{}');
			'''.format( 0,
				newMyData[0],
				newOpponentData[0],
				newMyData[1],
				newOpponentData[1],
				newMyData[1] - oldMyData[1],
				newOpponentData[1] - oldOpponentData[1],
				gameComment ))
	if gameResult == "draw": #если ничья
		cursor.execute('''
			INSERT INTO match (result, first_player_id, second_player_id, first_player_elo, second_player_elo, first_elo_change, second_elo_change, commentary)
			VALUES ({}, {}, {}, {}, {}, {}, {}, '{}');
			'''.format( -1,
				newMyData[0],
				newOpponentData[0],
				newMyData[1],
				newOpponentData[1],
				newMyData[1] - oldMyData[1],
				newOpponentData[1] - oldOpponentData[1],
				gameComment ))

	db.commit() #отправляем изменения
	return "OK"
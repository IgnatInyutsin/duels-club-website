import os
from flask import Flask, jsonify, request
import app
import database

def main(data):
	# Подключаемся к БД
	db = database.init()
	#устанавливаем курсор
	cursor = db.cursor()
	# Делаем запрос если в data значение рейтинг
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
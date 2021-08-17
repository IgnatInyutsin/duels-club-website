import os
import psycopg2

def init():
	#подключение к бд
	db = psycopg2.connect(
		database=os.environ['POSTGRES_DB'],
		user=os.environ['POSTGRES_USER'],
		password=os.environ['POSTGRES_PASSWORD'],
		host="pg_db",
		port="5432"
	)
	
	return db
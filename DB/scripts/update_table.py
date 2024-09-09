import mysql.connector
from dotenv import load_dotenv
import os
import json
import sys
load_dotenv()
rute = sys.argv[1]
print('Abriendo archivo json: ', rute)
with open(rute, "r") as file:
	data_json = json.load(file)
	conexion = mysql.connector.connect(
		host= os.getenv('DB_HOST'),
		user= os.getenv('DB_USER'),
		password= os.getenv('DB_PASSWORD'),
		database= "stats"
	)
	cursor = conexion.cursor()

	querys = data_json["querys"]
	data = data_json["data"]

	if "delete" in querys and querys["delete"]:
		print('Eliminando datos con query: ', querys["delete"])
		cursor.execute(querys["delete"])
		conexion.commit()

	if "insert" in querys and querys["insert"]:
		print('Insertando y/o updateando, query: ', querys["insert"])
		for data_insert in data["insert"]:
			print('Datos: ', data_insert)
			cursor.execute(querys["insert"], data_insert)
			conexion.commit()

	# En caso de querer hacer cualquier ejecucion extra se agrega en la tabla de query una query y en la de 
	for key in querys:
		if key != "delete" and key != "insert":
			if key in data and data[key]:
				print('Ejecutando extra query: ', data[key])
				for extra_data in data[key]:
					print('Datos: ', extra_data)
					cursor.execute(querys[key], extra_data)
					conexion.commit()

cursor.close()
conexion.close()

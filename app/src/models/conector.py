import mysql.connector
from dotenv import load_dotenv
import os

class ConectorBase:
	def __init__(self):
		load_dotenv()
		self.connection = mysql.connector.connect(
			host= os.getenv('DB_HOST'),
			user= os.getenv('DB_USER'),
			password= os.getenv('DB_PASSWORD'),
			database= "stats"
		)
		self.cursor = self.connection.cursor()
		self.columnas_name = []

	def execute_query(self, query, values = None):
		self.cursor.execute(query, values)
		self.connection.commit()
		id = self.cursor.lastrowid
		self.close()
		return id

	def select(self, query, values = None, select_one = 0):
		self.cursor.execute(query, values)
		results = self.cursor.fetchone() if select_one else self.cursor.fetchall()
		datos_dict = None if select_one else []
		if results:
			self.load_column_attr()
			datos_dict = dict(zip(self.columnas_name, results)) if select_one else [dict(zip(self.columnas_name, fila)) for fila in results]
			self.close()
		return datos_dict

	def load_column_attr(self):
		description_tabla = self.cursor.description
		for columna_desc in description_tabla:
			col_name = columna_desc[0]
			self.columnas_name.append(col_name)

	def select_one(self, query, values = None):
		return self.select(query, values, 1)

	def close(self):
		self.cursor.close()
		self.connection.close()

import mysql.connector
from dotenv import load_dotenv
import os

class conectorBase:
	def __init__(self):
		load_dotenv()
		self.connection = mysql.connector.connect(
			host= os.getenv('DB_HOST'),
			user= os.getenv('DB_USER'),
			password= os.getenv('DB_PASSWORD'),
			database= "stats"
		)
		self.cursor = self.connection.cursor()
		self.columnasName = []

	def executeQuery(self, query, values = None):
		self.cursor.execute(query, values)
		self.connection.commit()
		id = self.cursor.lastrowid
		self.close()
		return id

	def select(self, query, values = None, selectOne = 0):
		self.cursor.execute(query, values)
		results = self.cursor.fetchone() if selectOne else self.cursor.fetchall()
		datos_dict = None if selectOne else []
		if results:
			self.loadColumnAttr()
			datos_dict = dict(zip(self.columnasName, results)) if selectOne else [dict(zip(self.columnasName, fila)) for fila in results]
			self.close()
		return datos_dict

	def loadColumnAttr(self):
		descriptionTabla = self.cursor.description
		for columnaDesc in descriptionTabla:
			colName = columnaDesc[0]
			self.columnasName.append(colName)

	def selectOne(self, query, values = None):
		return self.select(query, values, 1)

	def close(self):
		self.cursor.close()
		self.connection.close()
from src.models.conector import conectorBase
from src.helpers.msgsHandler import msgsHandler
from src.models.MainClass import MainClass
import datetime

class Stock(MainClass):
	_table = "equity"
	_attrs = {
		"id": {
			"type": int,
			"postAdd": True,
		},
		"ticket": {
			"type": str,
		},
		"ppc": {
			"type": float,
		},
		"quantity": {
			"type": int,
		},
		"weighted_date": {
			"type": int,
		},
		"name": {
			"type": str
		},
		"ratio": {
			"type": int,
			"null" : True
		},
	}

	def __init__(self, data):
		super().__init__(data)

#--------------------------------------------------------METODOS ESTATICOS--------------------------------------------------------------#
	@staticmethod
	def findAll():
		conector = conectorBase()
		stock = []
		query = "SELECT s.*, t.ratio as ratio, t.name as name from " + Stock._table + " s JOIN tickets t ON (s.ticket = t.ticket) ORDER BY s.ticket"
		filas = conector.select(query)
		for fila in filas:
			stock.append(Stock(fila))
		return stock


	@staticmethod
	def findByTicket(ticket):
		conector = conectorBase()
		query = "SELECT s.*, t.ratio as ratio, t.name as name from " + Stock._table + " s JOIN tickets t ON (s.ticket = t.ticket) where s.ticket = %s"
		fila = conector.selectOne(query, [ticket])
		if fila:
			return Stock(fila)
		return None

	@staticmethod
	def ticketVerification(ticket):
		conector = conectorBase()
		query = "SELECT ratio, name FROM tickets WHERE ticket = %s"
		ticketData = conector.selectOne(query, [ticket])
		if ticketData:
			return {}, ticketData
		else:
			return {"ERROR_ATTR_INCORRECTO" : [[ticket]]}, {"ratio" : None, "name" : None}

	@staticmethod
	def add(data):
		errors, ticketData = Stock.ticketVerification(data["ticket"])
		attrsData = {**data, **ticketData}
		errors = Stock.preAddVerification(attrsData, errors)
		if len(errors) == 0:
			conector = conectorBase()
			values = [
				attrsData["ticket"],
				attrsData["ppc"],
				attrsData["quantity"],
				attrsData.get("weighted_date") or datetime.datetime.now().timestamp()
			]
			query = "INSERT INTO " + Stock._table + " (ticket, ppc, quantity, weighted_date) VALUES (%s, %s, %s, %s)"
			attrsData["id"] = conector.executeQuery(query, values)

			return Stock(attrsData)
		else:
			msgsHandler.printErrors(errors)
			return None

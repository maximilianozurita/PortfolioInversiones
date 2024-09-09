from src.models.conector import ConectorBase
from src.helpers.msgs_handler import msgsHandler
from src.models.main_class import MainClass
from src.models.ticket import Ticket
import datetime

class Stock(MainClass):
	_table = "equity"
	_attrs = {
		"id": {
			"type": int,
			"post_add": True,
		},
		"ticket_code": {
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
	def find_all():
		conector = ConectorBase()
		stock = []
		query = "SELECT s.*, t.ratio as ratio, t.name as name from " + Stock._table + " s JOIN tickets t ON (s.ticket_code = t.ticket_code) ORDER BY s.ticket_code"
		filas = conector.select(query)
		for fila in filas:
			stock.append(Stock(fila))
		return stock


	@staticmethod
	def find_by_ticket(ticket_code):
		conector = ConectorBase()
		query = "SELECT s.*, t.ratio as ratio, t.name as name from " + Stock._table + " s JOIN tickets t ON (s.ticket_code = t.ticket_code) where s.ticket_code = %s"
		fila = conector.select_one(query, [ticket_code])
		if fila:
			return Stock(fila)
		return None

	@staticmethod
	def add(data):
		errors, ticket_data = Ticket.check_ticket(data["ticket_code"], ["name", "ratio"])
		attrs_data = {**data, **ticket_data}
		errors = Stock.pre_check_add(attrs_data, errors)
		if len(errors) == 0:
			conector = ConectorBase()
			values = [
				attrs_data["ticket_code"],
				attrs_data["ppc"],
				attrs_data["quantity"],
				attrs_data.get("weighted_date") or datetime.datetime.now().timestamp()
			]
			query = "INSERT INTO " + Stock._table + " (ticket_code, ppc, quantity, weighted_date) VALUES (%s, %s, %s, %s)"
			attrs_data["id"] = conector.execute_query(query, values)

			return Stock(attrs_data)
		else:
			msgsHandler.print_errors(errors)
			return None

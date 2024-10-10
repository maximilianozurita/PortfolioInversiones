from src.models.conector import ConectorBase
from src.helpers.msgs_handler import msgsHandler
from src.models.main_class import MainClass
from src.models.ticket import Ticket

class History(MainClass):
	_table = "history"
	_attrs = {
		"id": {
			"type" : int,
			"post_add" : True,
		},
		"ticket_code": {
			"type": str,
			"column" : True
		},
		"ratio": {
			"type": int,
			"null" : True,
			"column" : True
		},
		"transaction_key": {
			"type": int,
			"null" : True,
			"column" : True
		},
		"broker_name": {
			"type": str,
			"null" : True,
			"column" : True
		},
		"quantity": {
			"type": int,
			"column" : True
		},
		"unit_price": {
			"type": float,
			"column" : True
		},
		"usd_quote": {
			"type": int,
			"column" : True
		},
		"date": {
			"type": int,
			"null" : True,
			"column" : True
		},
	}

	def __init__(self, data):
		super().__init__(data)

	@staticmethod
	def add(data):
		errors, ticket_data = Ticket.check_ticket(data["ticket_code"], ["ratio"])
		attrs_data = {**data, **ticket_data}
		errors = History.pre_check_add(attrs_data, errors)
		if len(errors) == 0:
			conector = ConectorBase()
			columns, values = History.get_query_params(attrs_data)
			query = "INSERT INTO " + History._table + " (" + ','.join(columns) + ") VALUES (" + ', '.join(['%s'] * len(columns)) + ")"
			attrs_data["id"] = conector.execute_query(query, values)
			return History(attrs_data), None
		else:
			msgsHandler.print_masivo(errors)
			return None, errors

	@staticmethod
	def find_by_id(id):
		conector = ConectorBase()
		query = "SELECT * from " + History._table + " where id = %s"
		fila = conector.select_one(query, [id])
		if fila:
			return History(fila)
		return None

	@staticmethod
	def find_all_by_ticket(ticket_code):
		conector = ConectorBase()
		history = []
		query = "SELECT * from " + History._table + " where ticket_code = %s"
		filas = conector.select(query, [ticket_code])
		for fila in filas:
			history.append(History(fila))
		return history

	@staticmethod
	def find_all():
		conector = ConectorBase()
		history = []
		query = "SELECT * from " + History._table
		filas = conector.select(query)
		for fila in filas:
			history.append(History(fila))
		return history


	@staticmethod
	def delete_by_id(id):
		conector = ConectorBase()
		query = "delete from " + History._table + " where id = %s"
		return conector.query_delete(query, [id])

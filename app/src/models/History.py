from src.models.conector import ConectorBase
from src.helpers.msgs_handler import msgsHandler
from src.models.main_class import MainClass
from src.models.ticket import Ticket
import datetime

class History(MainClass):
	_table = "history"
	_attrs = {
		"id": {
			"type": int,
			"post_add": True,
		},
		"ticket_code": {
			"type": str,
		},
		"ratio": {
			"type": int,
			"null" : True
		},
		"transaction_key": {
			"type": int,
			"null" : True
		},
		"broker_name": {
			"type": str,
			"null" : True
		},
		"quantity": {
			"type": int,
		},
		"unit_price": {
			"type": float,
		},
		"usd_quote": {
			"type": int,
		},
		"date": {
			"type": int,
			"null" : True
		},
	}

	def __init__(self, data):
		super().__init__(data)

	def add(data):
		errors, ticket_data = Ticket.check_ticket(data["ticket_code"], ["ratio"])
		attrs_data = {**data, **ticket_data}
		errors = History.pre_check_add(attrs_data, errors)
		if len(errors) == 0:
			conector = ConectorBase()
			values = [
				attrs_data["ticket_code"],
				attrs_data["ratio"],
				attrs_data["transaction_key"],
				attrs_data["broker_name"],
				attrs_data["quantity"],
				round(attrs_data["unit_price"], 4),
				attrs_data["usd_quote"],
				attrs_data["date"] or datetime.datetime.now().timestamp(),
			]
			query = "INSERT INTO " + History._table + " (ticket_code, ratio, transaction_key, broker_name, quantity, unit_price, usd_quote, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
			attrs_data["id"] = conector.execute_query(query, values)
			return History(attrs_data)
		else:
			msgsHandler.print_errors(errors)
			return None

	def find_by_id(id):
		conector = ConectorBase()
		query = "SELECT * from " + History._table + " where id = %s"
		fila = conector.select_one(query, [id])
		if fila:
			return History(fila)
		return None

	def find_all_by_ticket(ticket_code):
		conector = ConectorBase()
		history = []
		query = "SELECT * from " + History._table + " where ticket_code = %s"
		filas = conector.select(query, [ticket_code])
		for fila in filas:
			history.append(History(fila))
		return history

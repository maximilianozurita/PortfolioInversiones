from src.models.conector import ConectorBase
from src.utils.msgs_handler import msgsHandler
from src.models.main_class import MainClass
from src.models.ticket import Ticket
from src.models.transaction import Transaction

class Stock(MainClass):
	_table = "stock"
	_attrs = {
		"id": {
			"type": int,
			"post_add": True,
		},
		"ticket_code": {
			"type": str,
			"column" : True
		},
		"ppc": {
			"type": float,
			"column" : True
		},
		"quantity": {
			"type": int,
			"column" : True
		},
		"weighted_date": {
			"type": int,
			"column" : True
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
	def verify(data):
		errors, ticket_data = Ticket.check_ticket(data["ticket_code"], ["name", "ratio"])
		attrs_data = {**data, **ticket_data}
		errors = Stock.pre_check_add(attrs_data, errors)
		return attrs_data, errors


	@staticmethod
	def add(data):
		attrs_data, errors = Stock.verify(data)
		if len(errors) == 0:
			conector = ConectorBase()
			columns, values = Stock.get_query_params(data)
			query = "INSERT INTO " + Stock._table + " (" + ','.join(columns) + ") VALUES (" + ', '.join(['%s'] * len(columns)) + ")"
			attrs_data["id"] = conector.execute_query(query, values)
			return Stock(attrs_data), None
		else:
			msgsHandler.get_message_masivo(errors)
			return None, errors


	@staticmethod
	def update(data):
		attrs_data, errors = Stock.verify(data)
		if len(errors) == 0:
			conector = ConectorBase()
			query = 'UPDATE ' + Stock._table + ' (' + ','.join(data) + ') VALUES (' + ','.join(['%s'] * len(data)) + ')'
			values = [ data["ppc"], data["quantity"], data["weighted_date"], data["ticket_code"] ]
			attrs_data["id"] = conector.execute_query(query, values)
			return Stock(attrs_data), None
		else:
			msgsHandler.get_message_masivo(errors)
			return None, errors


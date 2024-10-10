from src.models.conector import ConectorBase
from src.helpers.msgs_handler import msgsHandler
from src.models.main_class import MainClass
from src.models.ticket import Ticket
from src.models.history import History

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

	def update(self, data):
		return 1


	# hay stock y quantity es negativo y mayor a stock quantity -> Error
	# hay stock y quiantity es negativo y menor a stock quantity -> updatear restando quantity
	# hay stock y quantity es negativo e igual a stock quantity -> eliminar stock
	def update_new_transaction(self, data):
		stock = None
		errors = {}
		quantity = self.quantity + data["quantity"]
		if quantity < 0:
			errors.setdefault("ERROR_ACCIONES_INSUFICIENTES", []).append([self.quantity, data["quantity"]])
		elif quantity == 0:
			self.delete()
		else:
			stock, errors = self.update(data)
			if len(errors) == 0:
				#generar data para history
				History.add(data)
		return stock, errors
		# if stock['quantity'] + data['quantity'] < 0:
		# 	print('No hay suficientes acciones para eliminar')
		# 	return {'error': 'no hay suficientes acciones para eliminar'}
		# else:
		# 	msg = ''
		# 	if stock['quantity'] + data['quantity'] == 0:
		# 		stockModel.delete_stock_holding(stock['ticket_code'])
		# 		msg = {'message': 'eliminado'}
		# 	else:
		# 		new_stock_holding = stockHelper.get_new_stock_holding_data(stock, data)
		# 		stockModel.set_stock_holding(new_stock_holding)
		# 		msg = {'message': 'eliminado'}
		# 	historyModel.set_transaction(data)
		# 	return msg
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
			columns, values = Stock.get_query_params(data)
			query = "INSERT INTO " + Stock._table + " (" + ','.join(columns) + ") VALUES (" + ', '.join(['%s'] * len(columns)) + ")"
			attrs_data["id"] = conector.execute_query(query, values)

			return Stock(attrs_data), None
		else:
			msgsHandler.get_message_masivo(errors)
			return None, errors

from src.models.stock import Stock
from src.models.transaction import Transaction
from src.utils.msgs_handler import msgsHandler

msgs = msgsHandler()
def add_transaction(data):
	_, errors = Transaction.verify(data)
	if len(errors) != 0:
		return { "ok": False, "msg": msgs.get_message_masivo(errors), "data": data}

	stock = Stock.find_by_ticket(data["ticket_code"])
	if stock:
		diff = stock.quantity + data["quantity"]
		if diff < 0:
			response = { "ok": False, "msg": msgs.get_message("ERROR_ACCIONES_INSUFICIENTES", [stock.quantity, data["quantity"]])}
		elif diff == 0:
			(_, errors) = Transaction.add(data)
			if errors:
				response = { "ok": False, "msg": msgs.get_message_masivo(errors)}
			else:
				stock.delete()
				response = {"ok": True, "msg": msgs.get_message("STOCK_DELETED")}
		else:
			(transaction, errors) = Transaction.add(data)
			data_stock = calculate_by_transaction(transaction, stock)
			(stock, errors) = stock.update(data_stock)
			if errors:
				response = { "ok": False, "msg": msgs.get_message_masivo(errors)}
			else:
				response = { "ok": True, "msg": msgs.get_message("STOCK_UPDATED"), "data": stock.get_attr_dict()}
	else:
		if data["quantity"] > 0:
			(transaction, errors) = Transaction.add(data)
			data_stock = calculate_by_transaction(transaction)
			(stock, errors) = Stock.add(data_stock)
			if errors:
				response = { "ok": False, "msg": msgs.get_message_masivo(errors)}
			else:
				response = { "ok": True, "msg": msgs.get_message("STOCK_ADDED"), "stock": stock.get_attr_dict()}
		else:
			response = { "ok": False, "msg": msgs.get_message("ERROR_ACCIONES_INSUFICIENTES", [0, data["quantity"]])}
	return response

def delete_transaction(id):
	data_response = {}
	if Transaction.delete_by_id(id):
		data_response = { "ok": True, "msg": msgs.get_message("ELEMENTO_ELIMINADO", [id])}
	else:
		data_response = { "ok": False, "msg": msgs.get_message("ERROR_ELIMINAR", [id])}
	return data_response


def get_transaction_by_id(id):
	transaction = Transaction.find_by_id(id)
	if transaction:
		return { "ok": True, "msg": msgs.get_message("ELEMENTO_ELIMINADO", [id]), "data": transaction.get_attr_dict()}
	else:
		return { "ok": False, "msg": msgs.get_message("NOT_FOUND")}


def get_transaction_list_by_ticket(ticket_code):
	data = []
	transaction_list = Transaction.find_all_by_ticket(ticket_code)
	for transaction in transaction_list:
		data.append(transaction.get_attr_dict())
	return {"ok": True, "data": data}


def get_transaction_list():
	data = []
	transaction_list =  Transaction.find_all()
	for transaction in transaction_list:
		data.append(transaction.get_attr_dict())
	return {"ok": True, "data": data}

def revert_transaction(id):
	transaction = Transaction.find_by_id(id)
	if transaction:
		stock = Stock.find_by_ticket(transaction.ticket_code)
		if stock:
			stock_data = calculate_revert_transaction(transaction, stock)
			(stock, errors) = stock.update(stock_data)
			if errors:
				response = { "ok": False, "msg": msgs.get_message_masivo(errors)}
			else:
				transaction.delete()
				response = { "ok": True, "msg": msgs.get_message("TRANSACCION_REVERTIDA"), "data": stock.get_attr_dict()}
		else:
			data_stock = calculate_by_transaction(transaction)
			(stock, errors) = Stock.add(data_stock)
			if errors:
				response = { "ok": False, "msg": msgs.get_message_masivo(errors)}
			else:
				response = { "ok": True, "msg": msgs.get_message("STOCK_ADDED"), "stock": stock.get_attr_dict()}
	else:
		response = { "ok": False, "msg": msgs.get_message("NOT_FOUND")}
	return response

def calculate_by_transaction(transaction, stock=None):
	data = {}
	if stock:
		quantity = stock.quantity + transaction.quantity
		if transaction.quantity > 0:
			data = {
				"quantity" : quantity,
				"ppc" : round((stock.ppc * stock.quantity + transaction.quantity * transaction.unit_price) / quantity, 4),
				"weighted_date" : int((stock.weighted_date * stock.quantity + transaction.quantity * transaction.date) / quantity)
			}
		elif transaction.quantity < 0:
			data = {
				"quantity" : quantity,
				"ppc" : stock.ppc,
				"weighted_date" : stock.weighted_date
			}
	else:
		data = {
			"ticket_code" : transaction.ticket_code,
			"quantity" : transaction.quantity,
			"ppc" : transaction.unit_price,
			"weighted_date" : transaction.date,
		}
	return data

def calculate_revert_transaction(transaction, stock):
	data = {}
	if transaction.quantity < 0:
		quantity = stock.quantity - transaction.quantity
		data = {
			"quantity" : quantity,
			"ppc" : stock.ppc,
			"weighted_date" : stock.weighted_date
		}
		return data
	elif transaction.quantity > 0:
		quantity = stock.quantity - transaction.quantity
		ppc = round((stock.ppc * stock.quantity - transaction.quantity * transaction.unit_price) / quantity, 4)
		weighted_date = int((stock.weighted_date * stock.quantity - transaction.quantity * transaction.date) / quantity)
		data = {
			"quantity" : quantity,
			"ppc" : ppc,
			"weighted_date" : weighted_date
		}

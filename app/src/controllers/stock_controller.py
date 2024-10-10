from src.models.stock import Stock
from src.models.history import History
from src.helpers.msgs_handler import msgsHandler

msgs = msgsHandler()
def _create_response(status: str, message, data=None,):
	response = {
		"status": status,
		"message": message,
		"data": data
	}
	return response

#Ver de crear objeto para manejo de errores y no solo para msgs genericos
def set_new_transaction(data):
	stock = Stock.find_by_ticket(data['ticket_code'])
	if stock:
		errors = stock.update_new_transaction(data)
		if len(errors) == 0:
			data, errors = History.add(data)
			return _create_response("Success", msgs.get_message("STOCK_UPDATED"), stock.get_attr_dict()), 200
		else:
			return _create_response("Error", msgs.get_message_masivo(errors), stock.get_attr_dict()), 500
	else:
		if data["quantity"] > 0:
			stock, errors = Stock.add(data)
			if len(errors) == 0:
				return _create_response("Success", msgs.get_message("STOCK_ADDED"), stock.get_attr_dict()), 200
			else:
				return _create_response("Error", msgs.get_message_masivo(errors), None), 500
		else:
			return _create_response("Error", msgs.get_message("ERROR_ACCIONES_INSUFICIENTES", [0, data["quantity"]]), None), 500


# def revert_transaction(id):
# 	data = historyModel.get_history(id)
# 	update_holding_stock(data, stockModel.get_hold_stock_by_ticket(data['ticket_code']))
# 	historyModel.delete_history(id)
# 	return {'message': 'eliminado'}


def delete_history(id):
	if History.delete_by_id(id):
		return _create_response("Success", msgs.get_message("ELEMENTO_ELIMINADO", [id]), None), 204
	else:
		return _create_response("Error", msgs.get_message("ERROR_ELIMINAR", [id]), None), 500


def get_history_by_id(id):
	history = History.find_by_id(id)
	if history:
		data = history.get_attr_dict()
		return _create_response("Ok", '', data), 200
	else:
		return _create_response("Not found", msgs.get_message("NOT_FOUND"), None), 404


def get_history_list_by_ticket(ticket_code):
	data = []
	history_list = History.find_all_by_ticket(ticket_code)
	for history in history_list:
		data.append(history.get_attr_dict())
	return _create_response("Ok", '', data), 200


def get_history_list():
	data = []
	history_list =  History.find_all()
	for history in history_list:
		data.append(history.get_attr_dict())
	return _create_response("Ok", '', data), 200


def get_stock_holding():
	data = []
	stocks = Stock.find_all()
	for stock in stocks:
		data.append(stock.get_attr_dict())
	return _create_response("Ok", '', data), 200


def update_holding_stock(data, stock):
	if stock['quantity'] + data['quantity'] < 0:
		print('No hay suficientes acciones para eliminar')
		return {'error': 'no hay suficientes acciones para eliminar'}
	else:
		msg = ''
		if stock['quantity'] + data['quantity'] == 0:
			stockModel.delete_stock_holding(stock['ticket_code'])
			msg = {'message': 'eliminado'}
		else:
			new_stock_holding = stockHelper.get_new_stock_holding_data(stock, data)
			stockModel.set_stock_holding(new_stock_holding)
			msg = {'message': 'eliminado'}
		historyModel.set_transaction(data)
		return msg

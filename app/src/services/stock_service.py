from src.models.stock import Stock
from src.models.transaction import Transaction
from src.utils.msgs_handler import msgsHandler
from src.services.service_base import _create_response

msgs = msgsHandler()
#Ver de crear objeto para manejo de errores y no solo para msgs genericos
def set_new_transaction(data):
	stock = Stock.find_by_ticket(data['ticket_code'])
	if stock:
		errors = stock.update_new_transaction(data)
		if len(errors) == 0:
			data, errors = Transaction.add(data)
			if len(errors) == 0:
				response = _create_response("Success", msgs.get_message("STOCK_UPDATED"), stock.get_attr_dict()), 200
			else:
				response = _create_response("Error", msgs.get_message_masivo(errors)), 500
		else:
			response = _create_response("Error", msgs.get_message_masivo(errors), stock.get_attr_dict()), 500
	else:
		if data["quantity"] > 0:
			stock, errors = Stock.add(data)
			if len(errors) == 0:
				response =  _create_response("Success", msgs.get_message("STOCK_ADDED"), stock.get_attr_dict()), 200
			else:
				response =  _create_response("Error", msgs.get_message_masivo(errors)), 500
		else:
			response =  _create_response("Error", msgs.get_message("ERROR_ACCIONES_INSUFICIENTES", [0, data["quantity"]]), None), 500
	return response

def get_stock_holding():
	data = []
	stocks = Stock.find_all()
	for stock in stocks:
		data.append(stock.get_attr_dict())
	return _create_response("Ok", '', data), 200


# def update_holding_stock(data, stock):
# 	if stock['quantity'] + data['quantity'] < 0:
# 		print('No hay suficientes acciones para eliminar')
# 		return {'error': 'no hay suficientes acciones para eliminar'}
# 	else:
# 		msg = ''
# 		if stock['quantity'] + data['quantity'] == 0:
# 			stockModel.delete_stock_holding(stock['ticket_code'])
# 			msg = {'message': 'eliminado'}
# 		else:
# 			new_stock_holding = stockHelper.get_new_stock_holding_data(stock, data)
# 			stockModel.set_stock_holding(new_stock_holding)
# 			msg = {'message': 'eliminado'}
# 		transactionModel.set_transaction(data)
# 		return msg

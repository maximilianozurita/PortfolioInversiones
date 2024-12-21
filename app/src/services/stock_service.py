from src.models.stock import Stock
from src.models.transaction import Transaction
from src.utils.msgs_handler import msgsHandler

msgs = msgsHandler()
def get_stock_holding():
	data = []
	stocks = Stock.find_all()
	for stock in stocks:
		data.append(stock.get_attr_dict())
	return { "ok": True,"data": data}

# =----------------------------ESTAS DEF SON DE EJEMPLO, NO SE USAN. SE USA LA PRIMERA
# def update_holding_stock(data):
# 	stock = Stock.find_by_ticket(data["ticket_code"])
# 	if stock:
# 		return stock.update_new_transaction(data)
# 	else:
# 		return {"ok": False, "msg": "No se encontro stock para ticket code"}
	# if stock['quantity'] + data['quantity'] < 0:
	# 	print('No hay suficientes acciones para eliminar')
	# 	return {'ok': False, 'msg': 'No hay suficientes acciones para eliminar, cantidad actual'}
	# else:
	# 	msg = ''
	# 	if stock['quantity'] + data['quantity'] == 0:
	# 		Stock.delete_stock_holding(stock['ticket_code'])
	# 		msg = {'message': 'eliminado'}
	# 	else:
	# 		new_stock_holding = stockHelper.get_new_stock_holding_data(stock, data)
	# 		Stock.set_stock_holding(new_stock_holding)
	# 		msg = {'message': 'eliminado'}
	# 	transactionModel.set_transaction(data)
	# 	return msg

# def set_new_transaction(data):
# 	stock = Stock.find_by_ticket(data['ticket_code'])
# 	if stock:
# 		errors = stock.update_new_transaction(data)
# 		if len(errors) == 0:
# 			data, errors = Transaction.add(data)
# 			if len(errors) == 0:
# 				response = { "ok": True, "msg": msgs.get_message("STOCK_UPDATED"), "data": stock.get_attr_dict()}
# 			else:
# 				response = { "ok": False, "msg": msgs.get_message_masivo(errors)}
# 		else:
# 			response = { "ok": False, "msg": msgs.get_message_masivo(errors), "data": stock.get_attr_dict()}
# 	else:
# 		if data["quantity"] > 0:
# 			stock, errors = Stock.add(data)
# 			if len(errors) == 0:
# 				response = { "ok": True, "msg": msgs.get_message("STOCK_ADDED"), "data": stock.get_attr_dict()}
# 			else:
# 				response = { "ok": False, "msg": msgs.get_message_masivo(errors)}
# 		else:
# 			response = { "ok": False, "msg": msgs.get_message("ERROR_ACCIONES_INSUFICIENTES", [0, data["quantity"]])}
# 	return response
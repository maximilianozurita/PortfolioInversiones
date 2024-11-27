from src.models.stock import Stock
from src.models.transaction import Transaction
from src.utils.msgs_handler import msgsHandler

msgs = msgsHandler()
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

# def revert_transaction(id): --> En lugar de eliminar la transaccion, revierte la transaccion y updatea la tenencia
# 	data = transactionModel.get_transaction(id)
# 	update_holding_stock(data, stockModel.get_hold_stock_by_ticket(data['ticket_code']))
# 	transactionModel.delete_transaction(id)
# 	return {'message': 'eliminado'}
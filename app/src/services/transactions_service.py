from src.models.stock import Stock
from src.models.transaction import Transaction
from src.utils.msgs_handler import msgsHandler
from src.services.service_base import _create_response

msgs = msgsHandler()
def delete_transaction(id):
	if Transaction.delete_by_id(id):
		return _create_response("Success", msgs.get_message("ELEMENTO_ELIMINADO", [id]), None), 204
	else:
		return _create_response("Error", msgs.get_message("ERROR_ELIMINAR", [id]), None), 500


def get_transaction_by_id(id):
	transaction = Transaction.find_by_id(id)
	if transaction:
		data = transaction.get_attr_dict()
		return _create_response("Ok", '', data), 200
	else:
		return _create_response("Not found", msgs.get_message("NOT_FOUND"), None), 404


def get_transaction_list_by_ticket(ticket_code):
	data = []
	transaction_list = Transaction.find_all_by_ticket(ticket_code)
	for transaction in transaction_list:
		data.append(transaction.get_attr_dict())
	return _create_response("Ok", '', data), 200


def get_transaction_list():
	data = []
	transaction_list =  Transaction.find_all()
	for transaction in transaction_list:
		data.append(transaction.get_attr_dict())
	return _create_response("Ok", '', data), 200

# def revert_transaction(id): --> En lugar de eliminar la transaccion, revierte la transaccion y updatea la tenencia
# 	data = transactionModel.get_transaction(id)
# 	update_holding_stock(data, stockModel.get_hold_stock_by_ticket(data['ticket_code']))
# 	transactionModel.delete_transaction(id)
# 	return {'message': 'eliminado'}
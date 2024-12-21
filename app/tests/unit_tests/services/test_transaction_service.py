import src.services.transaction_service as transaction_service
from tests.unit_tests.base import TestBase, unittest
from src.utils.msgs_handler import msgsHandler
from src.models.stock import Stock
from src.models.transaction import Transaction
import random
msgs = msgsHandler()

class TestTransactionService(TestBase):
	# def test_delete_transaction(self):
	# 	transaction = self.factory.get_new("Transaction")
	# 	response_expected = {
	# 		'msg': msgs.get_message("ELEMENTO_ELIMINADO", [transaction.id]),
	# 		'ok': True
	# 	}
	# 	response = transaction_service.delete_transaction(transaction.id)
	# 	self.assertDictEqual(response_expected, response)


	# def test_error_delete_transaction(self):
	# 	transaction = self.factory.get_new("Transaction")
	# 	response_expected = {
	# 		'msg': msgs.get_message("ERROR_ELIMINAR", [transaction.id]),
	# 		'ok': False
	# 	}
	# 	transaction.delete()
	# 	response = transaction_service.delete_transaction(transaction.id)
	# 	self.assertDictEqual(response_expected, response)


	# def test_get_transaction_by_id(self):
	# 	transaction = self.factory.get_new("Transaction")
	# 	response_expected = {
	# 		'msg': msgs.get_message("ELEMENTO_ELIMINADO", [transaction.id]),
	# 		'ok': True,
	# 		'data': transaction.get_attr_dict()
	# 	}
	# 	response = transaction_service.get_transaction_by_id(transaction.id)
	# 	self.assertDictEqual(response_expected, response)


	# def test_get_transaction_by_id_not_found(self):
	# 	response_expected = {
	# 		'msg': msgs.get_message("NOT_FOUND"),
	# 		'ok': False
	# 	}
	# 	transaction = self.factory.get_new("Transaction")
	# 	response = transaction_service.get_transaction_by_id(transaction.id + random.randint(1,10))
	# 	self.assertDictEqual(response_expected, response)


	# def test_get_transaction_list(self):
	# 	response_expected = {
	# 		'ok': True, 
	# 		'data': []
	# 	}
	# 	for i in range(5):
	# 		transaction = self.factory.get_new("Transaction")
	# 		response_expected["data"].append(transaction.get_attr_dict())
	# 	response = transaction_service.get_transaction_list()
	# 	self.assertDictEqual(response_expected, response)

	# def test_get_transaction_list_by_ticket(self):
	# 	response_expected = {
	# 		'ok': True, 
	# 		'data': []
	# 	}
	# 	for i in range(5):
	# 		self.factory.get_new("Transaction")
	# 	for i in range(5):
	# 		transaction = self.factory.get_new("Transaction", {"ticket_code" : "KO"})
	# 		response_expected["data"].append(transaction.get_attr_dict())
	# 	response = transaction_service.get_transaction_list_by_ticket("KO")
	# 	self.assertDictEqual(response_expected, response)
	# 	#list vacia
	# 	response_expected["data"] = []
	# 	response = transaction_service.get_transaction_list_by_ticket("MCD")
	# 	self.assertDictEqual(response_expected, response)

	# def test_add_positive_transaction_add_stock(self):
	# 	data_stock = self.factory.get_data_for('Stock')
	# 	data = {
	# 		'ticket_code' : data_stock['ticket_code'],
	# 		'quantity' : data_stock['quantity'],
	# 		'date' : data_stock['weighted_date'],
	# 		'unit_price' : data_stock['ppc'],
	# 		'usd_quote' : 10
	# 	}
	# 	response = transaction_service.add_transaction(data)
	# 	transactions = Transaction.find_all_by_ticket(data['ticket_code'])
	# 	for transaction in transactions:
	# 		self.factory.delete_on_cleanup(transaction)
	# 	stock = Stock.find_by_ticket(data['ticket_code'])
	# 	if stock: self.factory.delete_on_cleanup(stock)
	# 	self.assertTrue(response['ok'])
	# 	response_expected = {
	# 		'ok': True,
	# 		'msg': msgs.get_message("STOCK_ADDED"),
	# 		'stock': stock.get_attr_dict()
	# 	}
	# 	self.assertDictEqual(response_expected, response)

	# test agregar transaccion positiva updatea stock si ya hay stock
	def test_add_positive_transaction_update_stock(self):
		stock = self.factory.get_new("Stock")
		data = {
			'ticket_code' : stock.ticket_code,
			'quantity' : stock.quantity,
			'date' : stock.weighted_date,
			'unit_price' : stock.ppc,
			'usd_quote' : 10
		}
		response = transaction_service.add_transaction(data)
		print(response)
		transactions = Transaction.find_all_by_ticket(data['ticket_code'])
		for transaction in transactions:
			self.factory.delete_on_cleanup(transaction)
		stock = Stock.find_by_ticket(data['ticket_code'])
		if stock: self.factory.delete_on_cleanup(stock)
		self.assertTrue(response['ok'])
		response_expected = {
			'ok': True,
			'msg': msgs.get_message("STOCK_ADDED"),
			'stock': stock.get_attr_dict()
		}
		self.assertDictEqual(response_expected, response)

	# test agregar transaccion negativa updatea stock si ya hay stock
	# test error al agregar transaccion negativa sin stock
	# test error al agregar transaccion negativa si cantidad es menor
	# test agregar transaccion negativa elimina stock si cantidad es igual
	# test error al agregar transaccion con datos incorrectos


if __name__ == '__main__':
	unittest.main()
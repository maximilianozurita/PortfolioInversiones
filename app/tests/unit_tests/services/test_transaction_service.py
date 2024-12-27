import src.services.transaction_service as transaction_service
from tests.unit_tests.base import TestBase, unittest
from src.utils.msgs_handler import msgsHandler
from src.models.stock import Stock
from src.models.transaction import Transaction
import random
import copy
msgs = msgsHandler()

class TestTransactionService(TestBase):
	def test_delete_transaction(self):
		transaction = self.factory.get_new("Transaction")
		response_expected = {
			'msg': msgs.get_message("ELEMENTO_ELIMINADO", [transaction.id]),
			'ok': True
		}
		response = transaction_service.delete_transaction(transaction.id)
		self.assertDictEqual(response_expected, response)


	def test_error_delete_transaction(self):
		transaction = self.factory.get_new("Transaction")
		response_expected = {
			'msg': msgs.get_message("ERROR_ELIMINAR", [transaction.id]),
			'ok': False
		}
		transaction.delete()
		response = transaction_service.delete_transaction(transaction.id)
		self.assertDictEqual(response_expected, response)


	def test_get_transaction_by_id(self):
		transaction = self.factory.get_new("Transaction")
		response_expected = {
			'msg': msgs.get_message("ELEMENTO_ELIMINADO", [transaction.id]),
			'ok': True,
			'data': transaction.get_attr_dict()
		}
		response = transaction_service.get_transaction_by_id(transaction.id)
		self.assertDictEqual(response_expected, response)


	def test_get_transaction_by_id_not_found(self):
		response_expected = {
			'msg': msgs.get_message("NOT_FOUND"),
			'ok': False
		}
		transaction = self.factory.get_new("Transaction")
		response = transaction_service.get_transaction_by_id(transaction.id + random.randint(1,10))
		self.assertDictEqual(response_expected, response)


	def test_get_transaction_list(self):
		response_expected = {
			'ok': True, 
			'data': []
		}
		for i in range(5):
			transaction = self.factory.get_new("Transaction")
			response_expected["data"].append(transaction.get_attr_dict())
		response = transaction_service.get_transaction_list()
		self.assertDictEqual(response_expected, response)

	def test_get_transaction_list_by_ticket(self):
		response_expected = {
			'ok': True, 
			'data': []
		}
		for i in range(5):
			self.factory.get_new("Transaction")
		for i in range(5):
			transaction = self.factory.get_new("Transaction", {"ticket_code" : "KO"})
			response_expected["data"].append(transaction.get_attr_dict())
		response = transaction_service.get_transaction_list_by_ticket("KO")
		self.assertDictEqual(response_expected, response)
		#list vacia
		response_expected["data"] = []
		response = transaction_service.get_transaction_list_by_ticket("MCD")
		self.assertDictEqual(response_expected, response)

	def test_add_positive_transaction_add_stock(self):
		data = self.factory.get_data_for('Transaction')
		response = transaction_service.add_transaction(data)
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

	def test_add_positive_transaction_update_stock(self):
		stock = self.factory.get_new("Stock")
		old_stock = copy.deepcopy(stock)
		data = self.factory.get_data_for('Transaction', {'ticket_code' : stock.ticket_code})
		response = transaction_service.add_transaction(data)
		transactions = Transaction.find_all_by_ticket(data['ticket_code'])
		for transaction in transactions:
			self.factory.delete_on_cleanup(transaction)
		stock = Stock.find_by_ticket(data['ticket_code'])
		if stock: self.factory.delete_on_cleanup(stock)
		self.assertTrue(response['ok'])
		response_expected = {
			'ok': True,
			'msg': msgs.get_message("STOCK_UPDATED"),
			'data': stock.get_attr_dict()
		}
		self.assertDictEqual(response_expected, response)
		self.assertEqual(stock.ppc, round((old_stock.ppc * old_stock.quantity + data['quantity'] * data['unit_price']) / (old_stock.quantity + data['quantity']), 4))

	def test_add_negative_transaction_update_stock(self):
		stock = self.factory.get_new("Stock")
		old_stock = copy.deepcopy(stock)
		data = self.factory.get_data_for('Transaction', {'ticket_code' : stock.ticket_code, 'quantity' : -1})
		response = transaction_service.add_transaction(data)
		transactions = Transaction.find_all_by_ticket(data['ticket_code'])
		for transaction in transactions:
			self.factory.delete_on_cleanup(transaction)
		stock = Stock.find_by_ticket(data['ticket_code'])
		if stock: self.factory.delete_on_cleanup(stock)
		self.assertTrue(response['ok'])
		response_expected = {
			'ok': True,
			'msg': msgs.get_message("STOCK_UPDATED"),
			'data': stock.get_attr_dict()
		}
		self.assertDictEqual(response_expected, response)
		self.assertEqual(stock.quantity, round((old_stock.quantity + data['quantity']), 4))

	def test_add_negative_transaction_delete_stock(self):
		stock = self.factory.get_new("Stock")
		data = self.factory.get_data_for('Transaction', {'ticket_code' : stock.ticket_code, 'quantity' : -stock.quantity})
		response = transaction_service.add_transaction(data)
		transactions = Transaction.find_all_by_ticket(data['ticket_code'])
		for transaction in transactions:
			self.factory.delete_on_cleanup(transaction)
			self._assert_transaction_data(transaction, data)
		stock = Stock.find_by_ticket(data['ticket_code'])
		self.assertFalse(stock)
		self.assertTrue(response['ok'])
		response_expected = {
			'ok': True,
			'msg': msgs.get_message("STOCK_DELETED"),
		}
		self.assertDictEqual(response_expected, response)

	def test_error_add_negative_transaction_no_stock(self):
		data = self.factory.get_data_for('Transaction', {'quantity' : -1})
		response = transaction_service.add_transaction(data)
		transactions = Transaction.find_all_by_ticket(data['ticket_code'])
		self.assertListEqual(transactions, [])
		stock = Stock.find_by_ticket(data['ticket_code'])
		self.assertFalse(stock)
		self.assertFalse(response['ok'])
		self.assertEqual(response['msg'], msgs.get_message("ERROR_ACCIONES_INSUFICIENTES", [0, data['quantity']]))

	def test_error_add_negative_transaction_less_quantity(self):
		stock = self.factory.get_new("Stock")
		data = self.factory.get_data_for('Transaction', {'ticket_code' : stock.ticket_code, 'quantity' : -stock.quantity - 1})
		response = transaction_service.add_transaction(data)
		transactions = Transaction.find_all_by_ticket(data['ticket_code'])
		self.assertListEqual(transactions, [])
		stock = Stock.find_by_ticket(data['ticket_code'])
		self.assertTrue(stock)
		self.assertFalse(response['ok'])
		self.assertEqual(response['msg'], msgs.get_message("ERROR_ACCIONES_INSUFICIENTES", [stock.quantity, data['quantity']]))

	def _assert_transaction_data(self, transaction, data):
		transaction_dict = transaction.get_attr_dict()
		transaction_dict.pop("id", None)
		transaction_dict.pop("ratio", None)
		transaction_dict = {key: value for key, value in transaction_dict.items() if value is not None}
		self.assertDictEqual(data,transaction_dict)


if __name__ == '__main__':
	unittest.main()
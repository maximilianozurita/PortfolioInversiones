import src.services.stock_service as stock_service
import src.services.transactions_service as transaction_service
from tests.unit_tests.base import TestBase, unittest
from src.utils.msgs_handler import msgsHandler
import random
msgs = msgsHandler()

class TestTransactionResource(TestBase):
	def test_delete_transaction(self):
		code_expected = 204
		response_expected = {
			'status': 'Success', 
			'data': None
		}
		transaction = self.factory.get_new("Transaction")
		response_expected['message'] = msgs.get_message("ELEMENTO_ELIMINADO", [transaction.id])
		response, code = transaction_service.delete_transaction(transaction.id)
		self.assertEqual(code_expected, code)
		self.assertDictEqual(response_expected, response)


	def test_error_delete_transaction(self):
		code_expected = 500
		response_expected = {
			'status': 'Error', 
			'data': None
		}
		transaction = self.factory.get_new("Transaction")
		response_expected['message'] = msgs.get_message("ERROR_ELIMINAR", [transaction.id])
		transaction.delete()
		response, code = transaction_service.delete_transaction(transaction.id)
		self.assertEqual(code_expected, code)
		self.assertDictEqual(response_expected, response)


	def test_get_transaction_by_id(self):
		code_expected = 200
		response_expected = {
			'status': 'Ok', 
			'message': '',
		}
		transaction = self.factory.get_new("Transaction")
		response_expected['data'] = transaction.get_attr_dict()
		response, code = transaction_service.get_transaction_by_id(transaction.id)
		self.assertEqual(code_expected, code)
		self.assertDictEqual(response_expected, response)


	def test_get_transaction_by_id_not_found(self):
		code_expected = 404
		response_expected = {
			'status': 'Not found', 
			'data': None
		}
		transaction = self.factory.get_new("Transaction")
		response_expected['message'] = msgs.get_message("NOT_FOUND")
		response, code = transaction_service.get_transaction_by_id(transaction.id + random.randint(1,10))
		self.assertEqual(code_expected, code)
		self.assertDictEqual(response_expected, response)


	def test_get_transaction_list(self):
		code_expected = 200
		response_expected = {
			'status': 'Ok', 
			'message': '',
			'data': []
		}
		for i in range(5):
			transaction = self.factory.get_new("Transaction")
			response_expected["data"].append(transaction.get_attr_dict())
		response, code = transaction_service.get_transaction_list()
		self.assertEqual(code_expected, code)
		self.assertDictEqual(response_expected, response)


	def test_get_transaction_list_by_ticket(self):
		code_expected = 200
		response_expected = {
			'status': 'Ok', 
			'message': '',
			'data': []
		}
		for i in range(5):
			self.factory.get_new("Transaction")
		for i in range(5):
			transaction = self.factory.get_new("Transaction", {"ticket_code" : "KO"})
			response_expected["data"].append(transaction.get_attr_dict())
		response, code = transaction_service.get_transaction_list_by_ticket("KO")
		self.assertEqual(code_expected, code)
		self.assertDictEqual(response_expected, response)
		#list vacia
		response_expected["data"] = []
		response, code = transaction_service.get_transaction_list_by_ticket("MCD")
		self.assertEqual(code_expected, code)
		self.assertDictEqual(response_expected, response)

if __name__ == '__main__':
	unittest.main()
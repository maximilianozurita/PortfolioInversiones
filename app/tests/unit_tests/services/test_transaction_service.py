import src.services.transaction_service as transaction_service
from tests.unit_tests.base import TestBase, unittest
from src.utils.msgs_handler import msgsHandler
import random
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

if __name__ == '__main__':
	unittest.main()
import src.controllers.stock_controller as stock_controller
from tests.unit_tests.base import TestBase, unittest
from src.helpers.msgs_handler import msgsHandler
import random
msgs = msgsHandler()

class TestStockController(TestBase):
	def test_delete_history(self):
		code_expected = 204
		response_expected = {
			'status': 'Success', 
			'data': None
		}
		history = self.factory.get_new("History")
		response_expected['message'] = msgs.get_message("ELEMENTO_ELIMINADO", [history.id])
		response, code = stock_controller.delete_history(history.id)
		self.assertEqual(code_expected, code)
		self.assertDictEqual(response_expected, response)


	def test_error_delete_history(self):
		code_expected = 500
		response_expected = {
			'status': 'Error', 
			'data': None
		}
		history = self.factory.get_new("History")
		response_expected['message'] = msgs.get_message("ERROR_ELIMINAR", [history.id])
		history.delete()
		response, code = stock_controller.delete_history(history.id)
		self.assertEqual(code_expected, code)
		self.assertDictEqual(response_expected, response)


	def test_get_history_by_id(self):
		code_expected = 200
		response_expected = {
			'status': 'Ok', 
			'message': '',
		}
		history = self.factory.get_new("History")
		response_expected['data'] = history.get_attr_dict()
		response, code = stock_controller.get_history_by_id(history.id)
		self.assertEqual(code_expected, code)
		self.assertDictEqual(response_expected, response)


	def test_get_history_by_id_not_found(self):
		code_expected = 404
		response_expected = {
			'status': 'Not found', 
			'data': None
		}
		history = self.factory.get_new("History")
		response_expected['message'] = msgs.get_message("NOT_FOUND")
		response, code = stock_controller.get_history_by_id(history.id + random.randint(1,10))
		self.assertEqual(code_expected, code)
		self.assertDictEqual(response_expected, response)


	def test_get_history_list(self):
		code_expected = 200
		response_expected = {
			'status': 'Ok', 
			'message': '',
			'data': []
		}
		for i in range(5):
			history = self.factory.get_new("History")
			response_expected["data"].append(history.get_attr_dict())
		response, code = stock_controller.get_history_list()
		self.assertEqual(code_expected, code)
		self.assertDictEqual(response_expected, response)


	def test_get_stock_holding(self):
		code_expected = 200
		response_expected = {
			'status': 'Ok', 
			'message': '',
			'data': []
		}
		for i in range(5):
			stock = self.factory.get_new("Stock")
			response_expected["data"].append(stock.get_attr_dict())
		response, code = stock_controller.get_stock_holding()
		self.assertEqual(code_expected, code)
		self.assertDictEqual(response_expected, response)


if __name__ == '__main__':
	unittest.main()
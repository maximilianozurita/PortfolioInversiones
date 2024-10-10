from src.models.history import History
from src.models.ticket import Ticket
from src.helpers.msgs_handler import msgsHandler
from tests.unit_tests.base import TestBase, unittest
import random

class TestHistory(TestBase):
	def test_add_history(self):
		ticket_obj = Ticket("AAPL")
		data = {
			"ticket_code" : ticket_obj.ticket_code,
			"transaction_key" : random.randint(1,1000),
			"broker_name" : "IOLA",
			"quantity" : random.randint(1,100),
			"unit_price" : round(random.uniform(1,100), 4),
			"usd_quote" : random.randint(1,100),
			"date" : random.randint(1,1000)
		}
		(history, errors) = History.add(data)
		self.assertIsNone(errors)
		self.assertIsInstance(history, History)
		self.factory.delete_on_cleanup(history)
		for val in data: 
			self.assertEqual(data[val], getattr(history, val))
		objts = History.find_all_by_ticket(data["ticket_code"])
		self.assertIn(history,objts)


	def test_error_pre_check_add(self):
		ticket_obj = Ticket("AMD")
		data = {
			"ticket_code" : ticket_obj.ticket_code,
			"transaction_key" : "pp",
			"broker_name" : 1.2 ,
			"quantity" : "b",
			"date" : "a",
			"ratio": "cincuenta"
		}
		error_expected = {
			'ERROR_ATTR_TYPE': [['ratio', 'int', 'str'], ['transaction_key', 'int', 'str'], ['broker_name', 'str', 'float'], ['quantity', 'int', 'str'], ['date', 'int', 'str']], 
			'ERROR_ATTR_NONE': [['unit_price'], ['usd_quote']]
		}
		self.generic_test_check_add(History, data, False , error_expected)


	def test_error_post_check_add(self):
		data = {
			"name" : 1,
			"ratio": "cincuenta"
		}
		error_expected = {'ERROR_ATTR_NONE': [['id']]}
		self.generic_test_check_add(History, data, True , error_expected)


	def test_post_check_add_ok(self):
		data = {"id" : random.randint(1,100)}
		self.generic_test_check_add(History, data, True)


	def test_pre_check_add_ok(self):
		ticket_obj = Ticket("AMD")
		data = {
			"ticket_code" : ticket_obj.ticket_code,
			"transaction_key" : random.randint(1,1000),
			"broker_name" : "IOLA",
			"quantity" : random.randint(1,100),
			"unit_price" : round(random.uniform(1,100), 4),
			"usd_quote" : random.randint(1,100),
			"date" : random.randint(1,1000)
		}
		self.generic_test_check_add(History, data, False)


	def test_find_by_id(self):
		obj_expected = self.factory.get_new("History")
		obj = History.find_by_id(obj_expected.id)
		self.assertIsInstance(obj, History)
		self.assert_objs_equals(obj_expected, obj)


	def test_find_all_by_ticket(self):
		objs_expected = []
		ticket_code = Ticket("AMD").ticket_code
		for i in range(3):
			objs_expected.append(self.factory.get_new("History", {"ticket_code" :  ticket_code}))
		objs_finded = History.find_all_by_ticket(ticket_code)
		for i, obj in enumerate(objs_finded):
			self.assertIsInstance(obj, History)
			self.assert_objs_equals(objs_expected[i], obj)


	def test_delete(self):
		history = self.factory.get_new("History")
		history_id = history.id
		history.delete()
		obj = History.find_by_id(history_id)
		self.assertIsNone(obj)


	def test_delete_by_id(self):
		history = self.factory.get_new("History")
		History.delete_by_id(history.id)
		history = History.find_by_id(history.id)
		self.assertIsNone(history)


if __name__ == '__main__':
	unittest.main()

from tests.unit_tests.base import TestBase, unittest
from src.models.history import History
from src.models.ticket import Ticket
import random

class TestFactoryHistory(TestBase):
	def test_factory_creation(self):
		ticket_obj = Ticket("AAPL")
		data = {
			"ticket_code" : ticket_obj.ticket_code,
			"quantity" : random.randint(1,10),
			"transaction_key" : random.randint(1,1000),
			"usd_quote" : random.randint(1,1000),
			"unit_price" : round(random.uniform(1.0,20.0), 4)
		}

		obj = self.factory.get_new("History", data)
		self.assertIsInstance(obj, History)
		for val in data:
			self.assertEqual(data[val], getattr(obj, val))


	def test_creation_with_default_value(self):
		obj = self.factory.get_new("History")
		self.assertIsInstance(obj, History)
		attrs_expected = History.get_attrs_keys()
		for attr in attrs_expected:
			self.assertTrue(attr in obj.__dict__)

if __name__ == '__main__':
	unittest.main()
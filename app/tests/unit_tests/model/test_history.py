from src.models.history import History
from src.models.ticket import Ticket
from src.helpers.msgs_handler import msgsHandler
from tests.unit_tests.base import testBase, unittest
import random

class TestHistory(testBase):
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
		history = History.add(data)
		self.assertIsInstance(history, History)
		self.factory.delete_on_cleanup(history)
		for val in data: 
			self.assertEqual(data[val], getattr(history, val))
		objts = History.find_all_by_ticket(data["ticket_code"])
		self.assertIn(history,objts)

	# def testPreVerification(self):
	# def testPostAddVerification(self):
	# def testFindAll(self):
	# def testFindByTicket(self):
	# def testDelete(self):
	# def testFindById(self):

if __name__ == '__main__':
	unittest.main()

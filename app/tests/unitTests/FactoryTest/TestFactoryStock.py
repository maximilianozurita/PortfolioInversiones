from tests.unitTests.Base import testBase, unittest
from src.models.Stock import Stock
from src.models.Ticket import Ticket
import random

class testFactoryStock(testBase):
	def testCreacionFactory(self):
		ticketObj = Ticket("AAPL")
		data = {
			"ticket" : ticketObj.ticket,
			"ppc" : round(random.uniform(1.0,20.0), 4),
			"quantity" : random.randint(1,10),
			"weighted_date" : random.randint(1,1000)
		}
		try :
			objt = self.factory.getNew("Stock", data)
			self.assertIsInstance(objt, Stock)
			for val in data:
				self.assertEqual(data[val], getattr(objt, val))
		finally:
			objt.delete()

	def testCreacionConValoresDefault(self):
		try :
			objt = self.factory.getNew("Stock")
			self.assertIsInstance(objt, Stock)
			for attr in dir(objt):
				if not attr.startswith('__'):
					self.assertIsNotNone(getattr(objt, attr))
		finally:
			objt.delete()

if __name__ == '__main__':
	unittest.main()

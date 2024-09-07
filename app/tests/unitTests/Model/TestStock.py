from src.models.Stock import Stock
from src.models.Ticket import Ticket
from tests.unitTests.Base import testBase, unittest
import random

class testStock(testBase):
	def testAddStock(self):
		ticketObj = Ticket("AAPL")
		data = {
			"ticket" : ticketObj.ticket,
			"ppc" : round(random.uniform(1.0,20.0), 4),
			"quantity" : random.randint(1,10),
			"weighted_date" : random.randint(1,1000)
		}
		stock = Stock.add(data)
		self.assertIsInstance(stock, Stock)
		for val in data: 
			self.assertEqual(data[val], getattr(stock, val))
		objt = Stock.findByTicket(data["ticket"])
		self.assertAttrsEquals(objt, stock)
		self.factory.deleteOnCleanup(objt)

	def testPreAddVerification(self):
		ticketObj = Ticket("AMD")
		data = {
			"ticket" : ticketObj.ticket,
			"ppc" : "pp",
			"quantity" : 1.2 ,
			"weighted_date" : "a"
		}
		errors = Stock.preAddVerification(data)
		self.assertTrue(bool(errors))

	def testPostAddVerification(self):
		data = {
			"name" : 1,
			"ratio": "cincuenta"
		}
		errors = Stock.postAddVerification(data)
		self.assertTrue(bool(errors))

	def testFindAll(self):
		ticketsOjbs = Ticket.findAll()[:3]
		objsExpected = []
		for ticketObj in ticketsOjbs:
			objCreated = self.factory.getNew("Stock", {"ticket": ticketObj.ticket})
			objsExpected.append(objCreated)
		stockObj = Stock.findAll()
		for obj in stockObj:
			self.assertIsInstance(obj, Stock)
		self.assertEqual(len(objsExpected), len(stockObj))
		self.assertAttrsEquals(objsExpected[0], stockObj[0])
		self.assertAttrsEquals(objsExpected[1], stockObj[1])
		self.assertAttrsEquals(objsExpected[2], stockObj[2])

	def testFindByTicket(self):
		ticket = Ticket.findOne().ticket
		objExpected = self.factory.getNew("Stock", {"ticket": ticket})
		obj = Stock.findByTicket(ticket)
		self.assertIsInstance(obj, Stock)
		self.assertAttrsEquals(objExpected, obj)

	def testAttrCanBeNull(self):
		data = {
			"id" : random.randint(1,10),
			"name" : "nombrePrueba",
		}
		errors = Stock.postAddVerification(data)
		self.assertFalse(bool(errors))

	def testDelete(self):
		ticket = Ticket.findOne().ticket
		stock = self.factory.getNew("Stock", {"ticket": ticket})
		stock.delete()
		obj = Stock.findByTicket(ticket)
		self.assertIsNone(obj)

	def testAddWithTicketIncorrect(self):
		data = {
			"ticket" : "IncorrectTicketName",
			"ppc" : round(random.uniform(1.0,20.0), 4),
			"quantity" : random.randint(1,10),
			"weighted_date" : random.randint(1,1000)
		}
		stock = Stock.add(data)
		self.assertIsNone(stock)

if __name__ == '__main__':
	unittest.main()
from src.models.Ticket import Ticket
from src.models.conector import conectorBase
from tests.unitTests.Base import testBase, unittest

class testTicket(testBase):
	def testInstanciarObjeto(self):
		cursor = conectorBase()
		attrsExpected = cursor.selectOne("select * from tickets limit 1")
		obj = Ticket(attrsExpected["ticket"])
		self.assertIsInstance(obj, Ticket)
		for key, value in attrsExpected.items():
			self.assertTrue(hasattr(obj, key))
			self.assertEqual(getattr(obj, key), value)


	def testFindAll(self):
		tickets = Ticket.findAll()
		self.assertGreater(len(tickets), 0)
		for ticket in tickets:
			self.assertIsInstance(ticket, Ticket)

	def testFindOne(self):
		ticketObj = Ticket.findOne()
		self.assertIsInstance(ticketObj, Ticket)

	def testNoInstanciarTicketIncorrecto(self):
		TicketObj = Ticket("TicketIncorrecto")
		self.assertIsNone(TicketObj)

if __name__ == '__main__':
	unittest.main()
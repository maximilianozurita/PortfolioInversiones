from src.models.conector import conectorBase
from tests.unitTests.Base import testBase, unittest

class testConector(testBase):
	def testSelectOne(self):
		expected = {
			"ticket": "AAPL",
			"name": "Apple",
			"ratio": 10,
			"date": 1725505084
		}
		conector = conectorBase()
		query = 'select * from tickets where ticket = %s'
		select = conector.selectOne(query, ["AAPL"])
		self.assertDictEqual(expected, select)
		expected["ratio"] += 1
		self.assertNotEqual(expected, select)

	def testSelectAll(self):
		expected = [{
			"ticket": "AAPL",
			"name": "Apple",
			"ratio": 10,
			"date": 1725505084
		}]
		conector = conectorBase()
		query = 'select * from tickets where ticket = %s'
		select = conector.select(query, ["AAPL"])
		self.assertListEqual(expected, select)
		expected[0]["ratio"] +=1
		self.assertNotEqual(expected, select)

	# def testExecuteQuery():
	# def testCargarAttrColumnas():
#FALTA MEJORAR TESTS MEJORANDO EXPECTED

if __name__ == '__main__':
	unittest.main()
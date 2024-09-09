from src.models.conector import ConectorBase
from tests.unit_tests.base import testBase, unittest

class TestConector(testBase):
	def test_select_one(self):
		expected = {
			"ticket_code": "AAPL",
			"name": "Apple",
			"ratio": 10,
			"date": 1725763904
		}
		conector = ConectorBase()
		query = 'select * from tickets where ticket_code = %s'
		select = conector.select_one(query, ["AAPL"])
		self.assertDictEqual(expected, select)
		expected["ratio"] += 1
		self.assertNotEqual(expected, select)

	def test_select_all(self):
		expected = [{
			"ticket_code": "AAPL",
			"name": "Apple",
			"ratio": 10,
			"date": 1725763904
		}]
		conector = ConectorBase()
		query = 'select * from tickets where ticket_code = %s'
		select = conector.select(query, ["AAPL"])
		self.assertListEqual(expected, select)
		expected[0]["ratio"] +=1
		self.assertNotEqual(expected, select)

	# def testExecuteQuery():
	# def testCargarAttrColumnas():
	#Mejorar expected de tests

if __name__ == '__main__':
	unittest.main()
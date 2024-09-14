from src.models.conector import ConectorBase
from tests.unit_tests.base import TestBase, unittest
from src.models.ticket import Ticket
import random

class TestConector(TestBase):
	def test_select_one(self):
		ticket_obj = Ticket("AAPL")
		expected = {
			"ticket_code" : ticket_obj.ticket_code,
			"transaction_key" : random.randint(1,1000),
			"broker_name" : "IOLA",
			"quantity" : random.randint(1,100),
			"unit_price" : round(random.uniform(1,100), 4),
			"usd_quote" : random.randint(1,100),
			"date" : random.randint(1,1000)
		}
		self.factory.get_new("History", expected)
		conector = ConectorBase()
		query = 'select * from history where ticket_code = %s'
		select = conector.select_one(query, ["AAPL"])
		expected["id"] = select["id"]
		expected["ratio"] = ticket_obj.ratio
		self.assertDictEqual(expected, select)
		expected["unit_price"] += 1
		self.assertNotEqual(expected, select)

	def test_select_all(self):
		ticket_obj = Ticket("AAPL")
		expected = {
			"ticket_code" : ticket_obj.ticket_code,
			"transaction_key" : random.randint(1,1000),
			"broker_name" : "IOLA",
			"quantity" : random.randint(1,100),
			"unit_price" : round(random.uniform(1,100), 4),
			"usd_quote" : random.randint(1,100),
			"date" : random.randint(1,1000)
		}
		self.factory.get_new("History", expected)
		conector = ConectorBase()
		query = 'select * from history where ticket_code = %s'
		select = conector.select(query, ["AAPL"])
		expected["id"] = select[0]["id"]
		expected["ratio"] = ticket_obj.ratio
		self.assertListEqual([expected], select)
		expected["ratio"] +=1
		self.assertNotEqual([expected], select)

	# def test_load_columns_attrs(self):
	# 	conector = ConectorBase()
	# 	conector.cursor.execute("delete from equity")
	# 	conector.cursor.execute("select * from equity")
	# 	conector.cursor.fetchall()
	# 	conector.load_column_attr()
	# 	print(conector.columnas_name)
	# def test_load_columns_attrs_one_row(self):
	# def test_load_columns_attrs_none_rows(self):
	


if __name__ == '__main__':
	unittest.main()
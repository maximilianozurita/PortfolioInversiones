from src.models.Stock import Stock
from tests.Factory.FactoryBase import FactoryBase
from src.models.Ticket import Ticket
import random

class StockFactory(FactoryBase):
	def __init__(self, data):
		super().__init__(data)
		self.pkg = Stock

	def attrParser(self, data):
		data["ticket"] = data.get("ticket") or Ticket.findOne().ticket
		data["ppc"] = data.get("ppc") or round(random.uniform(1.0,20.0), 4)
		data["quantity"] = data.get("quantity") or random.randint(1,10)
		data["weighted_date"] = data.get("weighted_date") or random.randint(1,1000)
		return data

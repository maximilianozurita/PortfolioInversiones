from src.models.conector import conectorBase
from src.helpers.msgsHandler import msgsHandler
from src.models.MainClass import MainClass
import datetime

class History(MainClass):
	_table = "history"
	_attrs = {
		"id": {
			"type": int,
			"postAdd": True,
		},
		"ticket": {
			"type": str,
		},
		"ratio": {
			"type": int,
			"null" : True,
			"postAdd": True
		},
		"transaction_key": {
			"type": int,
			"null" : True
		},
		"broker_name": {
			"type": str,
			"null" : True
		},
		"quantity": {
			"type": int,
		},
		"unit_price": {
			"type": float,
		},
		"usd_quote": {
			"type": int,
		},
		"date": {
			"type": int,
			"null" : True
		},
	}

	def __init__(self, data):
		super().__init__(data)

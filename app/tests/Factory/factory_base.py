import random
import string

class FactoryBase:
	def __init__(self, data):
		self.attrs = self.attr_parser(data)

	def attr_parser(self, data):
		return data

	def init_obj(self):
		return self.pkg.add(self.attrs)

	def get_random_string(length=10):
		characters = string.ascii_letters + string.digits
		return ''.join(random.choice(characters) for i in range(length))

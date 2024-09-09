class FactoryBase:
	def __init__(self, data):
		self.attrs = self.attr_parser(data)

	def attr_parser(self, data):
		return data

	def init_obj(self):
		return self.pkg.add(self.attrs)

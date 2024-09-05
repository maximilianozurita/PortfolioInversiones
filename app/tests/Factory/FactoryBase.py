class FactoryBase:
	def __init__(self, data):
		self.attrs = self.attrParser(data)

	def attrParser(self, data):
		return data

	def initObj(self):
		return self.pkg.add(self.attrs)

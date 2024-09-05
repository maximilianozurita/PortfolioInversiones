from tests.Factory.StockFactory import StockFactory
class FactoryRegister:
	_class = {
		"Stock": StockFactory
	}
	def __init__(self):
		self.createdObjects = []

	def getNew(self, className, data = {}):
		if className in FactoryRegister._class:
			objFactory = FactoryRegister._class[className](data)
			objtCreated = objFactory.initObj()
			self.deleteOnCleanup(objtCreated)
			return objtCreated

	def deleteOnCleanup(self, objtCreated):
		self.createdObjects.append(objtCreated)

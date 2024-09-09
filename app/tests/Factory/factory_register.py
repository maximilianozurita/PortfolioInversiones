from tests.factory.stock_factory import StockFactory
class FactoryRegister:
	_class = {
		"Stock": StockFactory
	}
	def __init__(self):
		self.created_objects = []

	def get_new(self, class_name, data = None):
		if data is None: data = {}
		if class_name in FactoryRegister._class:
			obj_factory = FactoryRegister._class[class_name](data)
			obj_created = obj_factory.init_obj()
			self.delete_on_cleanup(obj_created)
			return obj_created

	def delete_on_cleanup(self, obj_created):
		self.created_objects.append(obj_created)

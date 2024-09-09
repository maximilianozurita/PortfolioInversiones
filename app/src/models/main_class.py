from src.helpers.msgs_handler import msgsHandler
from src.models.conector import ConectorBase

class MainClass:
	def __init__(self, data):
		errors = self.post_check_add(data)
		if len(errors) == 0:
			for attr in self._attrs:
				if attr in data:
					value = data[attr]
					setattr(self, attr, value)
		else:
			msgsHandler.print_errors(errors)
			raise AttributeError("No se pudo crear objeto")

	#Define que attrs se consideran relevantes para saber si 2 objs son iguales 
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.__dict__ == other.__dict__
		return False

	#Permite visualizar mejor el objeto y sus attr
	def __repr__(self):
			attrs = ', '.join(f'{attr}={getattr(self, attr)}' for attr in vars(self))
			return self.__class__.__name__ + f'({attrs})'

	def delete(self):
		conector = ConectorBase()
		query = "delete from " + self._table + " where id = %s"
		conector.execute_query(query, [self.id])
		del self

#--------------------------------------------------------METODOS ESTATICOS--------------------------------------------------------------#

	@classmethod
	def pre_check_add(cls, data, errors = None):
		if errors is None: errors = {}
		return MainClass.check_add(data, cls._attrs, False, errors)

	@classmethod
	def post_check_add(cls, data, errors = None):
		if errors is None: errors = {}
		return MainClass.check_add(data, cls._attrs, True, errors)

	@staticmethod
	def check_add(data, class_attrs, post_add, errors):
		attrs = {}
		if post_add:
			attrs = {key: value for key, value in class_attrs.items() if 'post_add' in value}
		else:
			attrs = {key: value for key, value in class_attrs.items() if 'post_add' not in value}
		for key, attr_value in attrs.items():
			attr_type = attr_value["type"]
			can_be_null = "null" in attr_value
			if key in data:
				value = data[key]
				if not can_be_null and value is None:
					errors.setdefault("ERROR_ATTR_NONE", []).append([key])
				if not isinstance(value, attr_type):
					errors.setdefault("ERROR_ATTR_TYPE", []).append([key, attr_type.__name__, type(value).__name__])
			elif not can_be_null:
				errors.setdefault("ERROR_ATTR_NONE", []).append([key])
		return errors

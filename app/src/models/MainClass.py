from src.helpers.msgsHandler import msgsHandler
from src.models.conector import conectorBase

class MainClass:
	def __init__(self, data):
		errors = self.postAddVerification(data)
		if len(errors) == 0:
			for attr in self._attrs:
				if attr in data:
					value = data[attr]
					setattr(self, attr, value)
		else:
			msgsHandler.printErrors(errors)
			raise AttributeError("No se pudo crear objeto")

	def __repr__(self):
			attrs = ', '.join(f'{attr}={getattr(self, attr)}' for attr in vars(self))
			print(attrs)
			return self.__class__.__name__ + f'({attrs})'

	def delete(self):
		conector = conectorBase()
		query = "delete from " + self._table + " where id = %s"
		conector.executeQuery(query, [self.id])
		del self

#--------------------------------------------------------METODOS ESTATICOS--------------------------------------------------------------#

	@classmethod
	def preAddVerification(cls, data, errors = {}):
		return MainClass.addVerification(data, cls._attrs, 0, errors)

	@classmethod
	def postAddVerification(cls, data, errors = {}):
		return MainClass.addVerification(data, cls._attrs, 1, errors)

	@staticmethod
	def addVerification(data, classAttrs, postAdd, errors):
		attrs = {}
		if postAdd:
			attrs = {key: value for key, value in classAttrs.items() if 'postAdd' in value}
		else:
			attrs = {key: value for key, value in classAttrs.items() if 'postAdd' not in value}
		for key, value in attrs.items():
			attrType = value["type"]
			canBeNull = "null" in value
			if key in data:
				value = data[key]
				if not canBeNull and value is None:
					errors.setdefault("ERROR_ATTR_NONE", []).append([key])
				if not isinstance(value, attrType):
					errors.setdefault("ERROR_ATTR_TYPE", []).append([key, attrType.__name__, type(value).__name__])
			elif not canBeNull:
				errors.setdefault("ERROR_ATTR_NONE", []).append([key])
		return errors

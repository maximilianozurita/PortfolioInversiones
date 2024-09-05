import json

class msgsHandler:
	def __init__(self):
		self.messages = self.__load_messages('config/msgs_es.json')

	def __load_messages(self, json_file):
		with open(json_file) as file:
			return json.load(file)

	def getMessage(self, key, params = []):
		if isinstance(params, list):
			message = self.messages.get(key, "Unknown error")
			countParamns = message.count('{}')
			if len(params) == countParamns and len(params) != 0:
				message = message.format(*params) #Para reemplazar valores dinamicos
			elif (len(params) > countParamns):
				print("Hay params de mas")
				message = ''
			elif (len(params) < countParamns):
				print("Falta params")
				message = ''
		else:
			print("Params no es un array")
			message = ''
		return message

	@staticmethod
	def printErrors(errors):
		#Ver posibilidad de en lugar de printear, de devolver array de msj
		menssages = []
		msgs = msgsHandler()
		for key, values in errors.items():
			for params in values:
				menssages.append(msgs.getMessage(key, params))
				print(msgs.getMessage(key, params))
		return menssages
